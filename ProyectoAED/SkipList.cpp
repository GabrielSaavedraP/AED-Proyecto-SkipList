#include <iostream>
#include <vector>
#include <fstream>
#include <cstdlib>
#include <string>
#include <ctime>

using namespace std;

template <typename T>
struct Node {
    T value;
    vector<Node<T>*> forward;

    Node(T val, int level) : value(val), forward(level + 1, nullptr) {}
};

template <typename T>
class SkipList {
private:
    int maxLevel;
    int currentLevel;
    Node<T>* head;
    ofstream csvFile;
    int iteracion;

    int randomLevel() {
        int lvl = 0;
        while ((rand() % 2 == 0) && lvl < maxLevel) {
            lvl++;
        }
        return lvl;
    }

    // Función auxiliar para formatear los nombres de los nodos en el CSV
    string formatNode(Node<T>* node) {
        if (node == head) return "HEAD";
        if (node == nullptr) return "NULL";
        return to_string(node->value);
    }

    void logEvent(string operacion, T valor, string accion, int nivel, Node<T>* current, Node<T>* nextNode, string resultado) {
        if (csvFile.is_open()) {
            csvFile << iteracion++ << "," << operacion << "," << valor << ","
                    << accion << "," << nivel << "," << formatNode(current) << ","
                    << formatNode(nextNode) << "," << resultado << "\n";
        }
    }

public:
    SkipList(int maxLvl, const string& filename)
        : maxLevel(maxLvl), currentLevel(0), iteracion(1) {

        head = new Node<T>(T(), maxLevel);

        csvFile.open(filename);
        if (csvFile.is_open()) {
            csvFile << "Iteracion,Operacion,Valor,Accion,Nivel,Nodo_Actual,Nodo_Siguiente,Resultado\n";
        }
    }

    ~SkipList() {
        if (csvFile.is_open()) csvFile.close();
        // Liberación de memoria pendiente para evitar memory leaks
    }

    // 1. INSERCIÓN
    void insertElement(T value) {
        vector<Node<T>*> update(maxLevel + 1, nullptr);
        Node<T>* current = head;

        logEvent("INSERTAR", value, "INICIAR", currentLevel, current, current->forward[currentLevel], "INICIO_OPERACION");

        for (int i = currentLevel; i >= 0; i--) {
            while (current->forward[i] != nullptr && current->forward[i]->value < value) {
                logEvent("INSERTAR", value, "AVANZAR", i, current, current->forward[i], "MENOR_QUE");
                current = current->forward[i];
            }
            update[i] = current;
            logEvent("INSERTAR", value, "BAJAR", i, current, current->forward[i], "NIVEL_COMPLETADO");
        }

        current = current->forward[0];

        if (current == nullptr || current->value != value) {
            int rlevel = randomLevel();
            logEvent("INSERTAR", value, "CALCULAR_NIVEL", rlevel, nullptr, nullptr, "NIVEL_GENERADO_" + to_string(rlevel));

            if (rlevel > currentLevel) {
                for (int i = currentLevel + 1; i <= rlevel; i++) {
                    update[i] = head;
                }
                currentLevel = rlevel;
            }

            Node<T>* newNode = new Node<T>(value, rlevel);
            logEvent("INSERTAR", value, "INSERTAR_NODO", rlevel, newNode, nullptr, "NODO_CREADO");

            for (int i = 0; i <= rlevel; i++) {
                newNode->forward[i] = update[i]->forward[i];
                update[i]->forward[i] = newNode;
                logEvent("INSERTAR", value, "ACTUALIZAR_PUNTEROS", i, update[i], newNode, "ENLACE_LISTO");
            }
            logEvent("INSERTAR", value, "FIN_EXITO", currentLevel, newNode, nullptr, "OPERACION_COMPLETA");
        } else {
            logEvent("INSERTAR", value, "FIN_FALLO", 0, current, nullptr, "ELEMENTO_DUPLICADO");
        }
    }

    // 2. BÚSQUEDA
    bool searchElement(T value) {
        Node<T>* current = head;
        logEvent("BUSCAR", value, "INICIAR", currentLevel, current, current->forward[currentLevel], "INICIO_OPERACION");

        for (int i = currentLevel; i >= 0; i--) {
            while (current->forward[i] != nullptr && current->forward[i]->value < value) {
                logEvent("BUSCAR", value, "AVANZAR", i, current, current->forward[i], "MENOR_QUE");
                current = current->forward[i];
            }
            logEvent("BUSCAR", value, "BAJAR", i, current, current->forward[i], "NIVEL_COMPLETADO");
        }

        current = current->forward[0];

        if (current != nullptr && current->value == value) {
            logEvent("BUSCAR", value, "FIN_EXITO", 0, current, nullptr, "ENCONTRADO");
            return true;
        } else {
            logEvent("BUSCAR", value, "FIN_FALLO", 0, current, nullptr, "NO_ENCONTRADO");
            return false;
        }
    }

    // 3. ELIMINACIÓN
    void removeElement(T value) {
        vector<Node<T>*> update(maxLevel + 1, nullptr);
        Node<T>* current = head;

        logEvent("ELIMINAR", value, "INICIAR", currentLevel, current, current->forward[currentLevel], "INICIO_OPERACION");

        for (int i = currentLevel; i >= 0; i--) {
            while (current->forward[i] != nullptr && current->forward[i]->value < value) {
                logEvent("ELIMINAR", value, "AVANZAR", i, current, current->forward[i], "MENOR_QUE");
                current = current->forward[i];
            }
            update[i] = current;
            logEvent("ELIMINAR", value, "BAJAR", i, current, current->forward[i], "NIVEL_COMPLETADO");
        }

        current = current->forward[0];

        if (current != nullptr && current->value == value) {
            logEvent("ELIMINAR", value, "ELIMINAR_NODO", 0, current, nullptr, "NODO_ENCONTRADO");

            for (int i = 0; i <= currentLevel; i++) {
                if (update[i]->forward[i] != current) break;
                update[i]->forward[i] = current->forward[i];
                logEvent("ELIMINAR", value, "ACTUALIZAR_PUNTEROS", i, update[i], current->forward[i], "ENLACE_LISTO");
            }

            delete current;

            while (currentLevel > 0 && head->forward[currentLevel] == nullptr) {
                currentLevel--;
            }
            logEvent("ELIMINAR", value, "FIN_EXITO", currentLevel, nullptr, nullptr, "OPERACION_COMPLETA");
        } else {
            logEvent("ELIMINAR", value, "FIN_FALLO", 0, current, nullptr, "NO_ENCONTRADO");
        }
    }
};

int main() {
    srand(static_cast<unsigned>(time(0)));

    // Altura máxima de 3 niveles, se generará el archivo animacion.csv
    SkipList<int> miLista(3, "animacion.csv");

    // Casos de Inserción
    miLista.insertElement(10);
    miLista.insertElement(20);
    miLista.insertElement(5);

    // Caso Borde: Buscar un elemento que no existe
    miLista.searchElement(15);

    // Búsqueda exitosa
    miLista.searchElement(20);

    // Eliminación
    miLista.removeElement(10);

    cout << "El archivo CSV ha sido generado con todas las operaciones." << endl;
    return 0;
}