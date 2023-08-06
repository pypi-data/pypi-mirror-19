#include "sddapi.h"

SddNode* sdd_array_element(SddNode** arr, int element) {
    return arr[element];
}

int sdd_array_int_element(int* arr, int element) {
    return arr[element];
}

//SddLiteral* create_sdd_literal_array(int varcount, * literals, SddManager* m) {
//    SddLiteral* res = (SddLiteral*) malloc(varcount * sizeof(SddLiteral*));
//    for (int i=0; i<varcount; i++) {
//        res[i] = sdd_manager_literal(literals[i], m);
//    }
//    return res;
//}