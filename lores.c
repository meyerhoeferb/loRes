#include "stdio.h"
#include "defs.h"

int main() {
    allInit();

    int i = 0;  //FIXME
    for(i = 0; i < BRD_SQ_NUM; i++) {
        if(i % 10 == 0) {
            printf("\n");
        }
        printf("%5d", sq120ToSq64[i]);
    }
    printf("\n");
    printf("\n");

    for(i = 0; i < 64; i++) {
        if(i % 8 == 0) {
            printf("\n");
        }
        printf("%5d", sq64ToSq120[i]);
    }



    return 0;
}
