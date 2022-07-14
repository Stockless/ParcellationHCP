#include <stdio.h>
#include <stdlib.h>
#include "bundleTools.h"
#include "BundleTools.c"



int main(int argc, char *argv[]){//21 = 21 puntos
	if(argc!=4){
		printf("./sliceFivers infile outfile nslices\n");
		return -1;
	}

	struct bundle f1,f2;
	//struct bundle read_bundle(char* bunfile)
	
	printf("%s\n%s\n%i\nok\n",argv[1],argv[2],string2int(argv[3]));

	f1 = read_bundle(argv[1]);

	//struct bundle sliceFiber( struct bundle fibras, int sliceNum)
	f2= sliceFiber( f1, string2int(argv[3]));

	//void write_bundle(char* outfile, int32_t nfibers, int32_t* npoints, float** points)
	write_bundle(argv[2], f2.nfibers, f2.npoints, f2.points);


}







