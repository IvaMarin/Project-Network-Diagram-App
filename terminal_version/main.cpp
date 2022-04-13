#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <cmath>
#include <limits>
#include <algorithm>
#include <list>
#include <stack>


using namespace std;

const int INF = numeric_limits<int>::max();

int n, m;
vector<vector<int>> graph;
vector<int> early;
vector<int> late;
vector<int> reserve;

/*
    Можно убрать поиск кратчайшего пути, т.к. 
    все вершины на критическом пути имеют нулевой 
    диапазон их можно просто добавить в граф 
    и вывести все пути
*/

class AdjListNode {
    int v;
    int weight;
   
public:
    AdjListNode(int _v, int _w) {
        v = _v;
        weight = _w;
    }
    int getV() { return v; }
    int getWeight() { return weight; }
};
   
class Graph {
    int n;
   
    list<AdjListNode>* adj;
   
    void topologicalSortUtil(int v, vector<bool> visited, stack<int>& Stack);
   
public:
    Graph(int n); 
    ~Graph(); 
 
    void addEdge(int u, int v, int weight);
   
    vector<int> longestPath(int s);
    vector<int> longestPath_2(int s); // костыль
};
   
Graph::Graph(int n) {
    this->n = n;
    adj = new list<AdjListNode>[n];
}
 
Graph::~Graph() {
    delete [] adj;
}
 
 
void Graph::addEdge(int u, int v, int weight) {
    AdjListNode node(v, weight);
    adj[u].push_back(node); 
}
   
void Graph::topologicalSortUtil(int v, vector<bool> visited, stack<int>& Stack) {
    visited[v] = true;
   
    list<AdjListNode>::iterator i;
    for (i = adj[v].begin(); i != adj[v].end(); ++i) {
        AdjListNode node = *i;
        if (!visited[node.getV()])
            topologicalSortUtil(node.getV(), visited, Stack);
    }
   
    Stack.push(v);
}
   
vector<int> Graph::longestPath(int s) {
    stack<int> Stack;
    vector<int> dist(n);
    vector<int> p(n); 
   
    vector<bool> visited(n);
    for (int i = 0; i < n; i++)
        visited[i] = false;
   
    for (int i = 0; i < n; i++)
        if (visited[i] == false)
            topologicalSortUtil(i, visited, Stack);
   
    for (int i = 0; i < n; i++)
        dist[i] = -INF;
    dist[s] = 0;

    while (Stack.empty() == false) {
        int u = Stack.top();
        Stack.pop();
   
        list<AdjListNode>::iterator i;
        if (dist[u] != -INF) {
            for (i = adj[u].begin(); i != adj[u].end(); ++i) {
             
                if (dist[i->getV()] < dist[u] + i->getWeight()) {
                    dist[i->getV()] = dist[u] + i->getWeight();
                    p[i->getV()] = u;
                }
            }
        }
    }


    vector<int> path;
    for (int v = n-1; v != s; v = p[v])
        path.push_back(v);
    path.push_back(s);
    reverse(path.begin(), path.end());

    return path;
}

vector<int> Graph::longestPath_2(int s) {
    stack<int> Stack;
    vector<int> dist(n);
    vector<int> p(n); 
   
    vector<bool> visited(n);
    for (int i = 0; i < n; i++)
        visited[i] = false;
   
    for (int i = 0; i < n; i++)
        if (visited[i] == false)
            topologicalSortUtil(i, visited, Stack);
   
    for (int i = 0; i < n; i++)
        dist[i] = -INF;
    dist[s] = 0;

    while (Stack.empty() == false) {
        int u = Stack.top();
        Stack.pop();
   
        list<AdjListNode>::iterator i;
        if (dist[u] != -INF) {
            for (i = adj[u].begin(); i != adj[u].end(); ++i) {
                // тут единственное отличие от longestPath(): вместо < используем <=
                if (dist[i->getV()] <= dist[u] + i->getWeight()) {
                    dist[i->getV()] = dist[u] + i->getWeight();
                    p[i->getV()] = u;
                }
            }
        }
    }


    vector<int> path;
    for (int v = n-1; v != s; v = p[v])
        path.push_back(v);
    path.push_back(s);
    reverse(path.begin(), path.end());

    return path;
}


void format_graph() {
    graph.resize(n);
    for (int i = 0; i < n; ++i)
        graph[i].resize(n);
    
    for (int i = 0; i < n; ++i)
        for (int j = 0; j < n; ++j)
            graph[i][j] = -1;
}

void print_graph() {
    for (int i = 0; i < n; ++i) {
        cout << i << ": ";
        for (int j = 0; j < n; ++j)
            cout << graph[i][j] << ((j != n-1) ? ", " : ";");
        cout << endl;
    }
}

void find_t_p() {
    early.resize(n);
    early[0] = 0;
    for (int i = 1; i < n; ++i) {
        int max_t = 0;
        int cur_max_t;
        for (int j = 0; j < i; ++j) {
            if (graph[i][j] != -1) {
                cur_max_t = early[j] + graph[i][j];
                if (cur_max_t > max_t)
                    max_t = cur_max_t;
            }
        }
        early[i]= max_t;
    }
}

void find_t_n() {
    late.resize(n);
    late[n-1] = early[n-1];

    for (int i = n-2; i >= 0; --i) {
        int min_t = INF;
        int cur_min_t;
        
        for (int j = n-1; j >= i+1; --j) {
            if (graph[i][j] != -1) {
                cur_min_t = late[j] - graph[i][j];
                if (cur_min_t < min_t)
                    min_t = cur_min_t;
            }
        }
        late[i] = min_t;
    }
}

void find_R() {
    reserve.resize(n);

    for (int i = 0; i < n; ++i) 
        reserve[i] = late[i] - early[i];
}

void print_answer() {
    for (int i = 0; i < n; ++i) {
        cout << i << ": " << "t_p = " << early[i] 
                        << ", t_n = " << late[i]
                        << ", R = " << reserve[i] << endl;
    }  
}

void print_path(vector<int> path) {
    for (size_t i = 0; i < path.size(); ++i)
        cout << path[i] << ((i != path.size()-1) ? " -> ": "");
    cout << endl;
}


int main() {
    cin >> n >> m;

    Graph g(n);
    
    format_graph();

    int u, v ,time;
    for (int i = 0; i < m; ++i) {
        cin >> u >> v >> time;
        g.addEdge(u, v, time);
        graph[u][v] = time; 
        graph[v][u] = time;       
    }

    find_t_p();
    find_t_n();
    find_R();

    print_answer();
    cout << endl;

    vector<int> path_1 = g.longestPath(0);
    vector<int> path_2 = g.longestPath_2(0);
    
    if (path_1 != path_2) {
        cout << "Критические пути: " << endl;
        print_path(path_1);
        print_path(path_2);
    } else {
        cout << "Критический путь: " << endl;
        print_path(path_1);
    }
    cout << endl;

    return 0;
}