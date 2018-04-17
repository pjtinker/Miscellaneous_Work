#include <omp.h>
#include <iostream>
#include <stdio.h>
#include <stdlib.h>
#include <cstdlib>

using namespace std;
const int GRID_SIZE = 4;
void setSquare(short** &board)
{
    board[0][3] = 1;
    board[1][2] =1;
    board[2][1] =1;
    board[2][2] = 1;
}

void tenCellRow(short* &board, int board_size)
{
    board[7 * board_size + 11] = 1;
    board[7 * board_size + 12] = 1;
    board[7 * board_size + 13] = 1;
    board[7 * board_size + 14] = 1;
    board[7 * board_size + 15] = 1;
    board[7 * board_size + 16] = 1;
    board[7 * board_size + 17] = 1;
    board[7 * board_size + 18] = 1;
    board[7 * board_size + 19] = 1;
    board[7 * board_size + 20] = 1;
}
short *emptyBoard(int board_row, int board_col)
{
    short *board = new short [board_row * board_col];
    for (int i = 0; i < board_row; i++)
    {
        for (int k = 0; k < board_col; k++)
            board[i * board_col + k] = 0;
    }

    return board; //return the matrix
}
short *createBoard(int board_row, int board_col)
{

    short *board = new short[board_row * board_col];
    for (int i = 0; i < board_row; i++)
    {
        for (int k = 0; k < board_col; k++)
            board[i * board_col + k] = rand() % 2;
    }

    return board; //return the matrix
}

void printBoard(short* &board, int row, int col)
{
    for (int i = 0; i < row; ++i)
    {
        for (int j = 0; j < col; ++j)
            printf("%d ", board[i * col + j]);
        printf("\n");
    }
}

short determineFate(int current_state, int neighbor_count)
{
    int fate = 0;
    switch(current_state) 
    {
        case 0: 
            if(neighbor_count == 3)
            {
                fate = 1;
            }
            break;
        case 1:
            if(neighbor_count < 2)
            {
                fate = 0;
            }else if(neighbor_count <= 3)
            {
                fate = 1;
            }
            break;
    }
    return fate;
}

int main( int argc, char* argv[])
{
    if(argc != 4)
    {
        cout << "Usage ./a [# threads] [# generations] [size of board]" << endl;
		return -1;
    }
    srand(time(0));
    int num_generations = atoi(argv[2]);
    int board_size = atoi(argv[3]);
    int thread_num = atoi(argv[1]);
    int num_board_splits = board_size / thread_num;
    short* board_one = createBoard(board_size, board_size);
    //short *board_one = emptyBoard(board_size, board_size);
    //tenCellRow(board_one, board_size);
    short* board_two = emptyBoard(board_size, board_size);
    short* temp;
    
    double begin_time, end_time = 0.0;
    begin_time = omp_get_wtime();

    #pragma omp parallel num_threads(thread_num)
    {
        int begin = num_board_splits * omp_get_thread_num();
        int end = begin + num_board_splits - 1;
        for (int i = 0; i < num_generations; ++i)
        {

            for (int a = begin; a <= end; ++a)
            {

                for (int b = 0; b < board_size; ++b)
                {
                    // Iterate through all neighboring cells, searching for life.
                    int live_count = 0;
                    for (int c = -1; c <= 1; c++)
                    {
                        for (int d = -1; d <= 1; d++)
                        {
                            // 
                            int row = a + c;
                            int col = b + d;
                            if (row < 0)
                                row = board_size - 1;
                            if (row >= board_size)
                                row = 0;
                            if (col >= board_size)
                                col = 0;
                            if (col < 0)
                                col = board_size - 1;

                            live_count += board_one[row * board_size + col];
                        }
                    }
                    // Remove the current cell if it was alive.
                    live_count -= board_one[a * board_size + b];
                    board_two[a * board_size + b] = determineFate(board_one[a * board_size + b], live_count);
                }
            }
            #pragma omp single
            {
                // cout << "Generation: " << i << endl;
                // printBoard(board_one, board_size, board_size);
                temp = board_one;
                board_one = board_two;
                board_two = temp;
            }

        }

    }
    end_time = omp_get_wtime();
    cout << thread_num << " "<< board_size << " " <<  end_time - begin_time << endl;
    delete[] board_one;
    delete[] board_two;
}       