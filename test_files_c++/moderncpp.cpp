#include <iostream>
#include <memory>

using namespace std; 
const string NL = "\n";


class Widget {
    public: 

    Widget() { cout << "Default cotr \n"; }
    ~Widget() { cout << "Default destructor \n"; }

    Widget(const Widget&) { cout << "Copy cotr \n"; }
    Widget& operator=(const Widget&) { cout << "copy assign \n"; return *this; }

    Widget(Widget&&) noexcept { cout << "Move constructor \n"; }
    Widget& operator=(Widget&&) noexcept { cout << "Move assignment operator \n"; return *this; }

};

/* int main() {
    cout << "-- construct w1 --\n";
    Widget w1;

    cout << "-- copy construct w2 from w1 --\n";
    Widget w2 = w1;

    cout << "-- move construct w3 from std::move(w1) --\n";
    Widget w3 = std::move(w1);

    cout << "-- copy assign w2 = w3 --\n";
    w2 = w3;

    cout << "-- move assign w2 = std::move(w3) --\n";
    w2 = std::move(w3);

    cout << "-- end of main, destructors fire --\n";
}
*/


struct A {
    void printA() {
        cout << "Printing A \n";
    }
};
//
//int main() {
//
//   unique_ptr<A> p1(new A);
//   // Using a unique_ptr allows exclusive ownership. one unique_ptr can point to one address. 
//   // It also autodeletes upon desctruction so there is no need for an exclusive destructor function. 
//   p1->printA(); // Printing A
//
//   cout << p1.get() << NL; // <address0x4039tgm3r0if>
//
//   unique_ptr<A> p2 = move(p1);
//   
//   p2->printA(); // Printing A
//   cout << p1.get() << NL; // 0
//   cout << p2.get() << NL; // <address0x4039tgm3r0if>
//   
//
//   return 0; 
// }


int main() {
    auto resourceDel = [](int* p) {
        cout << "Custom deleting: " << *p << NL;
        delete p;
    };
    shared_ptr<int> sp1(new int(25), resourceDel);
    cout << *sp1 << NL;
    cout << sp1 << NL;

    // shared_ptr<int> sp2 = sp1;  // COPY: Shared ownership, both pointers point to the same address
    shared_ptr<int> sp2 = move(sp1); // MOVE: ownership is transferred, sp1 is empty. 
    cout << sp1 << NL;
    cout << sp1 << NL;
    cout << sp2 << NL;
}; // When new is created as new[] the default deleter will throw an error, that is when a 
   // customer deleter is smart to use alongside the pointer. 