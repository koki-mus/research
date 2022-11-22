#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#include "streamLines.h"

const double PI = 3.1415926535897932;

const double gridx = 513;
const double gridy = 1025;
const double lengx = 2.0*PI;
const double lengy = 2.0;

const double dx = lengx/(gridx-1);
const double dy = lengy/(gridy-1);

int mag = 20;

StreamLine *streamlines;

int main(int argc, char **argv){

  char *xfile = argv[1];
  char *yfile = argv[2];
  char *picfile = argv[3];


//  char xfile[] = "magfield1";
//  char yfile[] = "magfield2";
//  char picfile[] = "test.bmp";
 
 streamlines = new StreamLine;
 streamlines->setDebug(true);
 //-------
 int datax, datay;
 datax = 513; datay=1025;
 streamlines->setDatsize(datax, datay);
 streamlines->setDelta(dx, dy);
 // mag decide out image size.
 streamlines->setwh(datax, datay, mag);
 double div = dy*0.1;
 // rs ;runbequtta no keisann kaisuu
 int rs = 15000;
 streamlines->setStreamParam(div, rs);
 streamlines->allocMem();
//----
 streamlines->loadData(xfile, yfile);
 double sp[3];
 float color[4];
 color[0]=color[1]=color[2]=color[3]=1.0f;
 sp[0] = 3.14; sp[1] = 1.2;
 for(int i=0;i<20;i++){
   sp[1] = 0.1+0.1*i;
   streamlines->stream_line(sp, color);
 }
 streamlines->writeBmp(picfile);
 //----
 streamlines->freeMem();
 delete streamlines;
 return 0;
}
