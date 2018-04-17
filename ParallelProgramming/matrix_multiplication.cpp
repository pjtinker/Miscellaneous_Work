// Paul Tinker
// CSC 6740, Program 1

#include <omp.h>
#include <string>
#include <iostream>
#include <stdio.h>
#include <stdlib.h>
#include <string>
#include <ctime>
#include <cstdlib>

using namespace std;

double** createMatrix(int rows, int cols) 
{

	double** matrix = new double*[rows]; 
	// cout << "***Generated Matrix***" << endl;
	for (unsigned int i = 0; i < rows; i++) 
	{	
		matrix[i] = new double[cols];
		for(unsigned int k = 0; k < cols; k++) 
		{
			matrix[i][k] = (rand() % 10);
		}
	}
	
	return matrix;  //return the matrix
}

void printLastRow(int row, int col, double** &matrix)
{
	for(unsigned int i = 0; i < col; i++ )
	{
		cout << matrix[row - 1][i] << "\t";
	}
	cout << endl;
}
void printMatrix(int rows, int cols, double** &matrix)
{
	for(unsigned int i = 0; i < rows; i++)
	{
		for(unsigned int j = 0; j < cols; j++)
		{
			cout << matrix[i][j] << "\t";
		}
		cout << endl;
	}
}
void getDotProduct(int begin, int end, int matrix_size, double** &matrix_one, double** &matrix_two, double** &result_matrix)
{
	double local_result = 0.0;
	for(unsigned int i = begin; i <= end; i++)
	{
		for(unsigned int k = 0; k < matrix_size; k++)
		{
			for(unsigned int j = 0; j < matrix_size; j++)
			{
				local_result += matrix_one[i][j] * matrix_two[j][k];
			}
			result_matrix[i][k] = local_result;
			local_result = 0.0;
		}
		
	}

}

int main( int argc, char* argv[] ) 
{
	if(argc != 3)
	{
		cout << "Usage ./a [# threads] [size of matrix]" << endl;
		return -1;
	}
	srand(time(0));
	int matrix_size = atoi(argv[2]);
	int thread_num = atoi(argv[1]);

	double** matrix_one = createMatrix(matrix_size, matrix_size);
	double** matrix_two = createMatrix(matrix_size, matrix_size);
	double** result_matrix = createMatrix(matrix_size, matrix_size);
	int num_matrix_splits = matrix_size / thread_num;
	int remainder = matrix_size % thread_num;
	double begin_time, end_time = 0.0;
	begin_time = omp_get_wtime();
	#pragma omp parallel num_threads(thread_num)
	{
		int begin = num_matrix_splits * omp_get_thread_num();
		int end = begin + num_matrix_splits - 1;
		if(omp_get_thread_num() + 1 == omp_get_num_threads())
		{
			end += remainder;
		}

		getDotProduct(begin, end, matrix_size, matrix_one, matrix_two, result_matrix);
	
	}
	end_time = omp_get_wtime();
	cout << thread_num << ", " << matrix_size << ", " << end_time - begin_time << endl;
	//cout << "***********************************************" << endl;
	//printLastRow(matrix_size, matrix_size, result_matrix);
	return 0;
}