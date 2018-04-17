/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

import java.io.*;
import java.lang.Math;
import java.util.ArrayList;
import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.InputMismatchException;
import java.util.Scanner;

/**
 *
 * @author hemlo
 */
public class FFT {

    public static void main (String args[]) throws IOException
    {
       double x = 1;
       double y = 0;
       double xx = 1;
       double yy = 0;
       int choice = 0;
       String other = "";
       Boolean truth = false;
       Boolean p = false;
       Scanner scan = new Scanner(System.in);
       System.out.println("Polynomial Evaluation\n=========================");
       Polynomial poly = null;
       while(choice != 9)
       {
        try{
           System.out.println("Please make your selection from the following choices:\n\n\r1. Generate a random polynomial of specified size.\n2. Read a polynomial from a specified file.\n3. Write the current polynomial to a specified file.\n4. Evaluate the current polynomial using Naive method.\n5. Evaluate the current polynomial using Horner's method.\n6. Evaluate the current polynomial using the Fast Fourier Transform.\n7. Evaluate the polynomial using a hybrid exponentiation method.\n8. Timed run with all algorithms and sequence of randomly generated polynomials.\n9. Exit\n");
           choice = scan.nextInt();
           {

               switch (choice)
                {
                   case 1: System.out.print("Please enter the number of coefficients you would like to generate.  Must be a power of 2! ");
                           int response = scan.nextInt();
                           if((response & (response - 1)) != 0)
                           {
                               System.out.println("Value not a power of 2.  Try again.");
                               break;
                           }
                           poly = new Polynomial(response);
                           System.out.println("Polynomial generated: ");
                           poly.displayCoefficients();
                           p = true;
                           break;
                   case 2: 
                       
                       while(!truth)
                        {
                           System.out.print("Please enter the file name to open: ");             
                           other = scan.nextLine();
                           if(other.length() > 0)
                               truth = true;
                        }
                        try
                        {
                           poly = new Polynomial(other);
                           System.out.println("File opened.  Polynomial:");
                           poly.displayCoefficients();   
                           p = true;
                        }catch(FileNotFoundException fnfe)
                        {
                         System.out.println("File read error. " + fnfe.getMessage() + " Try again.");   
                        }
                        truth = false;
                        break;
                   case 3: if(!p)
                            {
                                System.out.println("No polynomial exists.  Please choose option 1 or 2.");
                                break;
                            }
                       
                       while(!truth)
                        {
                           System.out.print("Please enter the name of the file to write to.  Warning: file will be overwritten! ");            
                           other = scan.nextLine();
                           if(other.length() > 0)
                               truth = true;
                        }
                        try
                        {
                           poly.writeFile(other);
                           System.out.println("File " + other + " written.");
                          

                        }catch(IOException fnfe)
                        {
                         System.out.println("File write error. " + fnfe.getMessage() + " Try again.");   
                        }
                        truth = false;
                        break;  
                   case 4: if(!p)
                            {
                                System.out.println("No polynomial exists.  Please choose option 1 or 2.");
                                break;
                            }else
                            {
                                poly.naiveEval();
                                break;
                            }
                            
                       
                   case 5: if(!p)
                            {
                                System.out.println("No polynomial exists.  Please choose option 1 or 2.");
                                break;
                            }else{
                                poly.hornerEval();
                                break;
                                }
                       
                   case 6: if(!p)
                            {
                                System.out.println("No polynomial exists.  Please choose option 1 or 2.");
                                break;
                            }else
                             {
                                 try{
                                     poly.fft();
                                     break;
                                 }catch(ArrayIndexOutOfBoundsException aiobe)
                                 {
                                     System.out.println("The number of terms in this polynomial is not a power of 2.  FFT cannot be ran.");
                                     break;
                                 }
                             }
                   case 7: if(!p)
                            {
                                System.out.println("No polynomial exists.  Please choose option 1 or 2.");
                                break;                               
                            }else
                           {
                               poly.exponentiation();
                               break;
                           }
                   case 8: if(!p)
                            {
                                System.out.println("No polynomial exists.  Please choose option 1 or 2.");
                                break;                               
                            }else{
                           
                            while(!truth)
                            {
                               System.out.print("Please enter the name of the file to write to.  Data will be appended to file! ");            
                               other = scan.nextLine();
                               if(other.length() > 0)
                                   truth = true;
                            }
                             try
                             {
                               poly.timedRun(other);
                               System.out.println("File " + other + " written.");
                                break;
                            }catch(IOException fnfe)
                            {
                             System.out.println("File write error. " + fnfe.getMessage() + " Try again."); 
                             break;
                            }
                   }
                }
           }
        }catch(InputMismatchException ime)
        {
            System.out.println("Invalid input.  Try again.");
            scan.nextLine();
        }
           
       }   
    }
}