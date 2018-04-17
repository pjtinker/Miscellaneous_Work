#include <mpi.h>
#include <omp.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <time.h>
#include <assert.h>
#include <string>
#include <fstream>
#include <iostream>
#include <cstring>
#include <ncurses.h>

using namespace std;

//Cell Colors
#define UNDERPOPULATION COLOR_RED
#define SUSTAIN         COLOR_BLUE
#define OVERCROWDING    COLOR_CYAN
#define REPRODUCTION    COLOR_GREEN

//Ncurses pair numbers
#define UND_PAIR  1
#define SUS_PAIR  2
#define OVER_PAIR 3
#define REP_PAIR  4

#define TOP_HALO_TAG 0
#define BOTTOM_HALO_TAG 1

void printBoard(bool* board, int row, int col)
{  
    for(int i = 0; i < row; ++i)
    {
        for(int j = 0; j < col; ++j)
            printf("%d ", board[i * col + j]);
        printf("\n");
    }

}

void writeBoard(bool* board, char* filename, double time, int row, int col)
{
    ofstream myfile(filename);
    if(!myfile.is_open())
    {
        cerr << "Problem opening output file " << filename << endl;
        MPI_Finalize();
        exit(2);
    }
    for(int i = 0; i < row; ++i)
    {
        for(int j = 0; j < col; ++j)
            myfile << board[i * col + j];
        myfile << '\n';
    }
    myfile << "Run time: " << time;
    myfile.close();

}
void rowMajorMatrixZero(bool* &board, int rows, int cols)
{
    for(int i = 0; i < rows; ++i)
        for(int j = 0; j < cols; ++j)
            board[i * cols + j] = 0;
}


void getRowsAndCols(MPI_File *in, int* dimension_offset, int* rows, int* cols)
{
    char* dims = new char[20];
    MPI_File_read(*in, dims, 20, MPI_BYTE, MPI_STATUS_IGNORE);
    bool complete = false;
    char* actual = new char[20];
    while(!complete)
    {
        for(int i = 0; i < 20; ++i)
        {
            if(dims[i] == '\n')
            {
                *dimension_offset = i + 1;
                complete = true;
                break;
            }
            actual[i] = dims[i];
        }
    }
    string result(actual);
    std::size_t split_point = result.find(" ");
    *rows = atoi(result.substr(0, split_point).c_str());
    *cols = atoi(result.substr(split_point+1).c_str());
    delete[] dims;
    delete[] actual;
}
/**
    Parallel file read
*/
bool* readBoard(MPI_File *in, const int rank, const int comm_sz, int dimension_offset, int rows, int cols)
{

    char* input = (char*)malloc(sizeof(char*) * rows * cols * 2);
    bool * board = (bool*)malloc(sizeof(bool*) * (rows + 2)* cols);
    
    int offset = rows * cols * 2;
    int line_offset = (rank * offset) + dimension_offset;

    if(rank == 0)
        line_offset = dimension_offset;
    MPI_File_read_at(*in, line_offset, input, offset, MPI_BYTE, MPI_STATUS_IGNORE);

    int board_count = cols;
    for(int i = 0; i < offset; ++i)
    {
        if(input[i] != ' ' && input[i] != '\n')
        {
            board[board_count] = atoi(&input[i]);
            board_count++;

        }
    }
    MPI_File_close(in);
    free(input);
    return board;

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

void computeBoard(int num_threads, int num_rows, int cols, bool* current, bool* next)
{   
    #pragma omp parallel num_threads(num_threads)
    {
        int num_rows_per_thread = num_rows / num_threads;
        int begin = (num_rows_per_thread * omp_get_thread_num())+1;
        int end = begin + num_rows_per_thread;
        for(int a = begin; a < end; ++a)
        {
            //printf("A: %d\n", a);
            for(int b = 0; b < cols; ++b)
            {
                int live_count = 0;
                //printf("A: %d B: %d\n", a,b);
                for (int c = -1; c <= 1; c++)
                {
                    for (int d = -1; d <= 1; d++)
                    {

                        int row = a + c;
                        int col = b + d;
                        if (row < 0)
                            row = cols - 1;
                        if (row >= cols)
                            row = 0;
                        if (col >= cols)
                            col = 0;
                        if (col < 0)
                            col = cols - 1;

                        live_count += current[row * cols + col];
                    }
                }
                live_count -= current[a * cols + b];
                next[a * cols + b] = determineFate(current[a * cols + b], live_count);
            }
        }
    }
}
bool* readInputArray(char* file_name, int rank, int* rows, int* cols)
{
    bool* array = NULL;
        ifstream my_file;
        my_file.open(file_name);
        if(!my_file.is_open())
        {
            cerr << "Unable to open file: " << file_name << "!\nExiting..." << endl;
            MPI_Abort(MPI_COMM_WORLD, 1);
        }

        string dimensions;
        getline(my_file, dimensions);
        int idx = dimensions.find(" ");
        *rows = atoi(dimensions.substr(0, idx).c_str());
        *cols = atoi(dimensions.substr(idx+1).c_str());

        if(rank == 0)
        {
            int row_offset = 0;
            array = (bool*)malloc(sizeof(bool) * (*rows) * (*cols));
            assert(array != NULL);
            for(int i = 0; i < *rows; ++i)
                for(int j = 0; j < (*cols); ++j)
                {
                    row_offset = i * (*cols);
                    my_file >> array[row_offset + j];
                }
        }
        MPI_Barrier(MPI_COMM_WORLD);
    return array;
}
void distributeBoard(int rank, int comm_sz, int total_rows, int cols, int num_rows_per_process, bool* complete_board,  bool* &current_board, MPI_Request* request)
{
    current_board = (bool*)malloc(sizeof(bool*) * total_rows * cols);
    if(rank == 0)
    {
        for(int i = 1; i < comm_sz; ++i)
        {
            MPI_Isend(&complete_board[i * num_rows_per_process * cols], (cols * num_rows_per_process), MPI_BYTE, i, 0, MPI_COMM_WORLD, &request[i]);
        }
        memcpy(&current_board[total_rows], complete_board, (cols * num_rows_per_process * sizeof(bool)));
    }else
    {
        MPI_Irecv(&current_board[total_rows], (cols * num_rows_per_process), MPI_BYTE, 0, 0, MPI_COMM_WORLD, &request[rank]);
    }
    MPI_Barrier(MPI_COMM_WORLD);
}
void compileBoard(int rank, int comm_sz, int total_rows, int cols, int num_rows_per_process, bool* current_board, bool* &final_board, MPI_Request* request)
{
    if(rank == 0)
    {
        final_board = (bool*)malloc(sizeof(bool*) * total_rows * cols);
        for(int i = 1; i < comm_sz; ++i)
        {
            MPI_Irecv(&final_board[i * num_rows_per_process * cols], (cols * num_rows_per_process), MPI_BYTE, i, 0, MPI_COMM_WORLD, &request[i]);
        }

       memcpy(final_board, &current_board[total_rows], (cols * num_rows_per_process * sizeof(bool)));
        
    }else
    {
        MPI_Isend(&current_board[total_rows], (cols * num_rows_per_process), MPI_BYTE, 0, 0, MPI_COMM_WORLD, &request[rank]);
    }
    MPI_Barrier(MPI_COMM_WORLD);
}


int main( int argc, char* argv[])
{
    MPI_Init(&argc, &argv);
        if(argc < 6)
    {
        printf("Usage ./a [input file][# MPI processes] [# OMP threads] [# generations] [output file] optional: -b (graphical display)\n");
        MPI_Abort(MPI_COMM_WORLD, 1);
    }
    MPI_File in, out;
    int rank, comm_sz, window_h, window_w;
    double begin_time, end_time;

    MPI_Comm_size(MPI_COMM_WORLD, &comm_sz);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    if(rank == 0)
    {
        begin_time = MPI_Wtime();
    }
    MPI_Status status[comm_sz];
    MPI_Request request[comm_sz];

    WINDOW *game_window = NULL;
    
    int num_mpi_procs = atoi(argv[2]);
    int num_omp_threads = atoi(argv[3]);
    int num_generations = atoi(argv[4]);
    string output_file(argv[5]);
    bool display_board = false;
    omp_set_num_threads(num_omp_threads);
    if(argv[6])
    {
        display_board = true;
    }
    int total_rows, cols, dimension_offset, num_rows_per_process;
    /* Remnants of parallel file access */
    // int err = MPI_File_open(MPI_COMM_WORLD, argv[1], MPI_MODE_RDONLY, MPI_INFO_NULL, &in);
    // if(err)
    // {
    //     if (rank == 0)fprintf(stderr, "%s: Couldn't open file %s\n", argv[0], argv[1]);
    //     MPI_Finalize();
    //     exit(2);
    // }

    // getRowsAndCols(&in, &dimension_offset, &total_rows, &cols);


    
    bool* current_board = NULL;
    bool* complete_board = readInputArray(argv[1], rank, &total_rows, &cols);
    num_rows_per_process = total_rows/comm_sz;

    /* Another parallel file access remnant */
    //current_board = readBoard(&in, rank, comm_sz, dimension_offset, num_rows_per_process, cols);

    distributeBoard(rank, comm_sz, total_rows, cols, num_rows_per_process, complete_board, current_board, request);
    bool* next_board = (bool*)malloc(sizeof(bool*) * (num_rows_per_process + 2)* cols);
    assert(next_board != NULL);
    bool* temp = NULL;
    bool* final_board = NULL;
    int board_offset = num_rows_per_process * total_rows;
    if(rank == 0 && display_board)
    {
        if((game_window = initscr()) == NULL)
        {
            printf("Unable to generate graphics window.\nExiting...\n");
            MPI_Abort(MPI_COMM_WORLD, 1);
        }
        resizeterm(total_rows, cols);
        cbreak();
        noecho();
        nonl();
        curs_set(0);
        start_color();
        getmaxyx(game_window, window_h, window_w);
        init_pair(UND_PAIR,  UNDERPOPULATION, COLOR_BLACK);
        init_pair(SUS_PAIR,  SUSTAIN,         COLOR_BLACK);
        init_pair(REP_PAIR,  REPRODUCTION,    COLOR_BLACK);
        init_pair(OVER_PAIR, OVERCROWDING,    COLOR_BLACK);

    }

    for(int i = 0; i < num_generations; ++i)
    {
        if(rank == 0)
        {
            MPI_Isend(&current_board[total_rows], cols, MPI_BYTE, comm_sz - 1, BOTTOM_HALO_TAG, MPI_COMM_WORLD, &request[0]);
            MPI_Isend(&current_board[board_offset], cols, MPI_BYTE, rank + 1, TOP_HALO_TAG, MPI_COMM_WORLD, &request[1]);
            MPI_Irecv(current_board, cols, MPI_BYTE, comm_sz - 1, TOP_HALO_TAG, MPI_COMM_WORLD, &request[2]);
            MPI_Irecv(&current_board[board_offset + total_rows], cols, MPI_BYTE, rank + 1, BOTTOM_HALO_TAG, MPI_COMM_WORLD, &request[3]);

        }
        else if(rank == comm_sz - 1)
        {
            
            MPI_Isend(&current_board[total_rows], cols, MPI_BYTE, rank - 1, BOTTOM_HALO_TAG, MPI_COMM_WORLD, &request[0]);
            MPI_Isend(&current_board[board_offset], cols, MPI_BYTE, 0, TOP_HALO_TAG, MPI_COMM_WORLD, &request[1]);
            MPI_Irecv(current_board, cols, MPI_BYTE, rank - 1, TOP_HALO_TAG, MPI_COMM_WORLD, &request[2]);
            MPI_Irecv(&current_board[board_offset + total_rows], cols, MPI_BYTE, 0, BOTTOM_HALO_TAG, MPI_COMM_WORLD, &request[3]);
        }
        else
        {
            
            MPI_Isend(&current_board[total_rows], cols, MPI_BYTE, rank - 1, BOTTOM_HALO_TAG, MPI_COMM_WORLD, &request[0]);
            MPI_Isend(&current_board[board_offset], cols, MPI_BYTE, rank + 1, TOP_HALO_TAG, MPI_COMM_WORLD, &request[1]);
            MPI_Irecv(current_board, cols, MPI_BYTE, rank - 1, TOP_HALO_TAG, MPI_COMM_WORLD, &request[2]);
            MPI_Irecv(&current_board[board_offset + total_rows], cols, MPI_BYTE, rank + 1, BOTTOM_HALO_TAG, MPI_COMM_WORLD, &request[3]);
        }

        MPI_Waitall(4, request, status);
        computeBoard(num_omp_threads, num_rows_per_process, cols, current_board, next_board);

        temp = current_board;
        current_board = next_board;
        next_board = temp;

        MPI_Barrier(MPI_COMM_WORLD);
        /** 
            Display the board if the option was requested
        */
        if(display_board)
        {
            compileBoard(rank, comm_sz, total_rows, cols, num_rows_per_process, current_board, final_board, request);
            if(rank == 0)
            {
                for(int i = 0; i < total_rows; ++i)
                {
                    for(int j = 0; j < cols; ++j)
                    {
                        if(final_board[i * cols + j] == false)
                        {
                            attron(COLOR_PAIR(OVER_PAIR));
                            mvwaddch(game_window, i, j, 50);
                        }
                        else
                        {
                            attron(COLOR_PAIR(UND_PAIR));
                            mvwaddch(game_window, i,j,48);
                        }
                    }
                }
                refresh();
                usleep(50000);
            }
        }
    }
    // Next step is to combine everything from every thread then output time.  
    compileBoard(rank, comm_sz, total_rows, cols, num_rows_per_process, current_board, final_board, request);

    if(rank == 0)
    {
        if(display_board)
        {
            endwin();
        }
        end_time = MPI_Wtime();
        writeBoard(final_board, argv[5], (end_time - begin_time), total_rows, cols);
        printf("%d, %d, %f\n", comm_sz, total_rows, (end_time - begin_time)); 
        /* On larger board sizes, this call to free will crash on the HPC.  */
       // free(final_board);
    }

    MPI_Barrier(MPI_COMM_WORLD);
    MPI_Finalize();
    free(current_board);
    free(next_board);
}