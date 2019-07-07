// Questioner: Google
// Difficulty: Hard
/*
An XOR linked list is a more memory efficient doubly linked list. Instead of each node holding next and prev fields, it holds a field named both, which is an XOR of the next node and the previous node. Implement an XOR linked list; it has an add(element) which adds the element to the end, and a get(index) which returns the node at index.

If using a language that has no pointers (such as Python), you can assume you have access to get_pointer and dereference_pointer functions that converts between nodes and memory addresses.
*/
#include <iostream>
#include <stdexcept>

class Item {
  public:
  Item* both;

  int value;
  Item(int val) : value(val) {};
};

class List {
  Item* first;
  Item* last;

  public:
  void add(int value) {
    if (!last) { // list is empty
      first = last = new Item(value);
      first->both = nullptr;
    } else {
      Item* e = new Item(value);
      e->both = last;
      last->both = (Item*)((uintptr_t)last->both ^ (uintptr_t)e);
      last = e;
    }
  };

  int get(int index) {
    if (!first) {
      throw new std::out_of_range("No elements in list!");
    }
    Item* prev = nullptr;
    Item* item = first;
    for (int i = 0; item; i++) {
      if (i == index) {
        return item->value;
      }

      Item* next = (Item*)((uintptr_t)item->both ^ (uintptr_t)prev);
      prev = item;
      item = next;
    }
    throw new std::out_of_range("Out of range!");
  };
};

int main() {
  List* list = new List();
  for(int i = 0; i < 10; i++) {
    list->add(i);
  }
  for (int i = 0; i < 10; i++) {
    int actual = list->get(i);
    if (actual != i) {
      std::cout << "Item at index " << i << " was " << actual << "!" << std::endl;
    } else {
      std::cout << '.';
    }
  }

  return 0;
}