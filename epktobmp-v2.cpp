#include "libbmp.h"
#include <bits/stdc++.h>
using namespace std;

int grayrange = 50;
BmpImg color_block( BmpImg img,int cx, int cy, int n, bool color, bool gray){
	n = pow(2, n);
	cx *= n;
	cy *= n;
	int cv_w = 255,
		cv_b = 0;
	//--------- gray --------
	if(gray){
		cv_w = rand()%grayrange+128;
		cv_b = rand()%grayrange+(127-grayrange);
	}
	else{
		cv_w = 255;
		cv_b = 0;
	}
	//------------------------
	for(int y = cy; y < cy+n; y++){
		for(int x = cx; x < cx+n; x++){
			if(color == true) img.set_pixel(x, y, cv_w, cv_w, cv_w);
			else img.set_pixel(x, y, cv_b, cv_b, cv_b);
		}
	}
	return img;
}

int main(){
	string epk_input;
	cout << "Ethereum private key: "; cin >> epk_input;
	cout << "Select resolution:" <<endl;// Blocksize
	cout << "1. 16x16 px" <<endl;     	// 2^0
	cout << "2. 32x32 px" <<endl;     	// 2^1
	cout << "3. 64x64 px" <<endl;     	// 2^2
	cout << "4. 128x128 px" <<endl;   	// 2^3
	cout << "5. 256x256 px" <<endl;   	// 2^4
	cout << "6. 512x512 px" <<endl;   	// 2^5
	cout << "7. 1024x1024 px" <<endl; 	// 2^6
	cout << "8. 2048x2048 px" <<endl; 	// 2^7
	int n = 0;
	cout << "(1-8): "; cin >> n; n--;
	bool gray; string grayconfirm;
	//------------- Gray select -------------//
	cout << "Gray? (y/n): "; cin >> grayconfirm;
	if(grayconfirm == "" || grayconfirm == "n" || grayconfirm == "no" || grayconfirm == "N" || grayconfirm == "No"){
		cout << "Rendering as Black and White." <<endl;
		gray = false;
	}
	else if (grayconfirm == "y" || grayconfirm == "yes" || grayconfirm == "Y" || grayconfirm == "Yes"){
		cout << "Rendering as Gray." <<endl;
		gray = true;
	}
	//------------------- Length Check ----------------//
	if(epk_input.size() != 64 && epk_input.size() != 66){
		cout << "Incorrect private key length." <<endl;
		cout << "Your input was of length " << epk_input.size() <<endl;
		cout << "Ethereum private key length is 64." <<endl;
		return 0;
	}
	char eth_private_key[64];
	//----------------- 0x flag check -----------------//
	if(epk_input.size() == 66 && epk_input[0] == '0' && epk_input[1] == 'x'){
		for(int i = 0; i < 64; i++){
			eth_private_key[i] = epk_input[i+2];
		}
		cout <<endl;
	}
	else{
		for(int i = 0; i < 64; i++){
			eth_private_key[i] = epk_input[i];
		}
	}
	//----------------Hex to Decimal----------------//
	int decimal[64];
	for(int i = 0; i < 64; i++){
		if(int(eth_private_key[i]) > 96 && int(eth_private_key[i]) < 103) decimal[i] = int(eth_private_key[i])-87;
		else decimal[i] = int(eth_private_key[i]) - 48;
	}
	//----------------Decimal to Binary----------------//
	vector <bool> hexseg(4, 0);
	vector <bool> binary;
	int tempint;
	for(int i = 0; i < 64; i++){
		tempint = decimal[i];
		int cntr = 1;
		for(int i = 0; i < 4; i++) hexseg[i] = 0;
		while(tempint > 0){
			if(tempint % 2 == 1){
				hexseg[4-cntr] = 1;
				tempint = (tempint-1)/2;
			}
			else{
				hexseg[4-cntr] = 0;
				tempint/=2;
			}
			cntr++;
		}
		binary.insert(binary.end(), hexseg.begin(), hexseg.end());
	}
	cout << "Binary: ";
	for(int i = 0; i < 256; i++){
		if(i%4 == 0) cout << "  ";
		if(i%16 == 0) cout <<endl;
		
		if(binary[i] == true) cout << "1 ";
		else cout << "0 ";
	}cout <<endl;
	//---------------- Imaging ----------------//
	BmpImg image(16*pow(2, n), 16*pow(2, n));
	for(int y = 0; y < 16; y++){
		for(int x = 0; x < 16; x++){
			if(binary[(y*16)+x] == true) image = color_block(image, x, y, n, true, gray);
			else image = color_block(image, x, y, n, false, gray);
		}
	}
	string filename = "1234.bmp";
	for(int i = 0; i < 3; i++) filename[i] = epk_input[i];
	image.write(filename);
}