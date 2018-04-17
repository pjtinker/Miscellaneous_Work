#include <string>    //I use strings throughout the program
#include <iostream>  // iostream for input and output
#include <fstream>   // fstream for reading from a file
#include <vector>    // Vectors are used to store 
#include <stdlib.h>	 // stdlib for atoi conversion
#include <cstdlib>
#include <algorithm> //for shuffle
#include <stdexcept>
#include <map>
#include <sstream>
#include <ctime>
#include "GA.h"

using namespace std;


 
int** createMatrix(int n_city) {
	int** matrix = new int*[n_city ]; //init with number of cities for row & col
	for (int i = 0; i < n_city; i++) {	
		matrix[i] = new int[n_city];
	}
	for (int i = 0; i < n_city; i++) {
		for (int j = 0; j < n_city; j++) {//filling the matrix with zeros
			matrix[i][j] = 0;
		}
	}
	return matrix;  //return the matrix
}


void printMatrix(int** &mat)
{

}
int main(int argc, char *argv[])
	{
				srand (unsigned(time(0)));

		if(argc != 5)
		{
			cerr << "Usage [c_list] [d_list] [pop size] [num generations]" << endl;
			return 0;
		}
		string c;
		int count = 0;
		int num_pop = atoi(argv[3]);
		int num_gen = atoi(argv[4]);
		if(num_pop %10 != 0 || num_pop <= 0)
		{
			cerr << "Factor of 10 population required."<<endl;
			exit(1);
		}
		char delim = ' ';
		string start, dest, mileage;
		vector<int> cities;
		map<string, int> refer;
		ifstream c_list, d_list;
		c_list.open(argv[1]);
		d_list.open(argv[2]);
		
		if(!c_list.is_open()){
			cerr << "Problem opening city file." << endl;
			return 0;
		}
		if(!d_list.is_open()){
			cerr << "Problem opening distance file." << endl;
			return 0;
		}
	
		while(getline(c_list, c)){
			cities.push_back(count);
			refer[c] = count++;
		}
		cities.push_back(0);
		int** matrix = createMatrix(cities.size());

		while(getline(d_list, c)){
			istringstream ss(c);
			getline(ss, start, delim);
			getline(ss, dest, delim);
			getline(ss, mileage, delim);
			matrix[refer[start]][refer[dest]] = atoi(mileage.c_str());//populate matrix with distances

		}
		vector<Chromosome> first_pop;
		vector<int> mutate = cities;
		c_list.close();
		d_list.close();


		for(int i = 0; i < num_pop; i++)
		{
			shuffle(mutate);	
			Chromosome *chrom = new Chromosome(mutate, matrix);
			first_pop.push_back(*chrom);
			
		}

		Population population(first_pop);
		population.nextGen(matrix, num_gen, num_pop);
		population.getFittestChrom().printCities();
		cout << population.getFittestChrom().getFitness() << endl;
		
		
		return 0;
	}

