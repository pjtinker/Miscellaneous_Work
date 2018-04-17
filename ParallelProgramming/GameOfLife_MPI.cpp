#include <mpi.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <assert.h>
#include <string.h>


using namespace std;


void rowMajorMatrixZero(short* &board, int rows, int cols)
{
    for(int i = 0; i < rows; ++i)
        for(int j = 0; j < cols; ++j)
            board[i * cols + j] = 0;

}

void rowMajorMatrix(short* &board, int rows, int cols)
{
    for(int i = 0; i < rows; ++i)
        for(int j = 0; j < cols; ++j)
            board[i * cols + j] = (rand() % 2);

}

void printRowMajorMatrix(short* matrix, int row, int col)
{
    for(int i = 0; i < row; ++i)
    {
        for(int j = 0; j < col; ++j)
            printf("%d ", matrix[i * col + j]);
        printf("\n");
    }

}

void printArray(short* array, int array_size)
{
    for(int i = 0; i < array_size; ++i)
    {
        printf("%d ", array[i]);
    }
    printf("\n");
}

int determineFate(int current_state, int neighbor_count)
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

void computeBoard(int num_rows, int width, short* current, short* next)
{
    for(int a = 1; a <= num_rows; ++a)
    {
        for(int b = 0; b < width; ++b)
        {
            int live_count = 0;
            for (int c = -1; c <= 1; c++)
            {
                for (int d = -1; d <= 1; d++)
                {
                    //
                    int row = a + c;
                    int col = b + d;
                    if (row < 0)
                        row = width - 1;
                    if (row >= width)
                        row = 0;
                    if (col >= width)
                        col = 0;
                    if (col < 0)
                        col = width - 1;

                    live_count += current[row * width + col];
                }
            }
            live_count -= current[a * width + b];
            next[a * width + b] = determineFate(current[a * width + b], live_count);
        }
    }

}


int main( int argc, char* argv[])
{
    MPI_Init(&argc, &argv);
    if(argc != 3)
    {
        printf("Usage ./a [# generations] [size of board]\n");
        MPI_Abort(MPI_COMM_WORLD, 1);
    }
    int num_generations = atoi(argv[1]);
    int board_size = atoi(argv[2]);
    double begin_time, end_time;

    int comm_sz;
    int rank;
    MPI_Comm_size(MPI_COMM_WORLD, &comm_sz);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    begin_time = MPI_Wtime();
    MPI_Status status[comm_sz];
    MPI_Request request[comm_sz];
    int num_rows_per_process = board_size / comm_sz;
    srand((unsigned) time( NULL ) + rank);

    // Create current board and blank board for swap space with two additional rows for halo padding
    short* current_board = (short*)malloc(sizeof(short) * (num_rows_per_process + 2) * board_size);
    assert(current_board != NULL);
    rowMajorMatrix(current_board, num_rows_per_process + 2, board_size);
    // Code below generates a 10 row configuration to test the functionality of the algorithm.  
    // short ten_row[20] = {0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0};
    // if(rank == 0)
    // {
    //     memcpy(&current_board[board_size], &ten_row, board_size * sizeof(short));
    //     printRowMajorMatrix(current_board, num_rows_per_process + 2, board_size);
    // }
    short* next_board = (short*)malloc(sizeof(short) * (num_rows_per_process + 2) * board_size);
    assert(next_board != NULL);
    rowMajorMatrixZero(next_board, num_rows_per_process + 2, board_size);
    short* final_board = NULL;
    short* temp = NULL;

    int board_offset = num_rows_per_process * board_size;

    for(int i = 0; i < num_generations; ++i)
    {
        if(rank == 0)
        {
            MPI_Isend(&current_board[board_size], board_size, MPI_SHORT, comm_sz - 1, 0, MPI_COMM_WORLD, &request[0]);
            MPI_Isend(&current_board[board_offset], board_size, MPI_SHORT, rank + 1, 0, MPI_COMM_WORLD, &request[1]);
            MPI_Irecv(current_board, board_size, MPI_SHORT, comm_sz - 1, 0, MPI_COMM_WORLD, &request[2]);
            MPI_Irecv(&current_board[board_offset + board_size], board_size, MPI_SHORT, rank + 1, 0, MPI_COMM_WORLD, &request[3]);

        }else if(rank == comm_sz - 1)
        {
            
            MPI_Isend(&current_board[board_size], board_size, MPI_SHORT, rank - 1, 0, MPI_COMM_WORLD, &request[0]);
            MPI_Isend(&current_board[board_offset], board_size, MPI_SHORT, 0, 0, MPI_COMM_WORLD, &request[1]);
            MPI_Irecv(current_board, board_size, MPI_SHORT, rank - 1, 0, MPI_COMM_WORLD, &request[2]);
            MPI_Irecv(&current_board[board_offset + board_size], board_size, MPI_SHORT, 0, 0, MPI_COMM_WORLD, &request[3]);
        }
        else
        {
            MPI_Isend(&current_board[board_size], board_size, MPI_SHORT, rank - 1, 0, MPI_COMM_WORLD, &request[0]);
            MPI_Isend(&current_board[board_offset], board_size, MPI_SHORT, rank + 1, 0, MPI_COMM_WORLD, &request[1]);
            MPI_Irecv(current_board, board_size, MPI_SHORT, rank - 1, 0, MPI_COMM_WORLD, &request[2]);
            MPI_Irecv(&current_board[board_offset + board_size], board_size, MPI_SHORT, rank + 1, 0, MPI_COMM_WORLD, &request[3]);
        }
        MPI_Waitall(4, request, status);
        computeBoard(num_rows_per_process, board_size, current_board, next_board);
        temp = current_board;
        current_board = next_board;
        next_board = temp;
        // This may be unuseful
        MPI_Barrier(MPI_COMM_WORLD);
    }
    // Next step is to combine everything from every thread then output time.  
    if(rank == 0)
    {
        final_board = (short*)malloc(sizeof(short) * board_size * board_size);
        for(int i = 1; i < comm_sz; ++i)
        {
            MPI_Irecv(&final_board[i * num_rows_per_process * board_size], (board_size * num_rows_per_process), MPI_SHORT, i, 0, MPI_COMM_WORLD, &request[i]);
        }
        memcpy(final_board, &current_board[board_size], board_size * num_rows_per_process * sizeof(short));
        
    }else
    {
        MPI_Isend(&current_board[board_size], (board_size * num_rows_per_process), MPI_SHORT, 0, 0, MPI_COMM_WORLD, &request[rank]);
    }
    MPI_Barrier(MPI_COMM_WORLD);

    if(rank == 0)
    {
        //printf("Final board:\n");
        //printRowMajorMatrix(final_board, board_size, board_size);
        end_time = MPI_Wtime();
        printf("%d, %d, %f\n", comm_sz, board_size, (end_time - begin_time)); 
    }

    MPI_Finalize();
    free(current_board);
    free(next_board);
    free(final_board);
    return 0;
}       