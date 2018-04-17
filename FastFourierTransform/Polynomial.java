/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */


/**
 *
 * @author hemlo
 */
import java.util.Random;
import java.io.*;
import java.util.ArrayList;
import java.util.Arrays;
public class Polynomial 
{
    
    private int size;
    public ArrayList<Complex> poly;
    private BufferedReader br;
    private PrintWriter pw;
    private ArrayList<Long> runTimes;
    private ArrayList<Integer> opCounts;
    public long naive, exp, fft, horner = 0;
    public long startTime = 0;
    public long endTime = 0;
    public long totalTime = 0;
    public long ops = 0;
    public Polynomial(int n)
    {
        poly = Complex.genRandom(n);
        size = n;
        runTimes = new ArrayList<>();
        opCounts = new ArrayList<>();
        naive=exp=horner=fft = 0l;
    }
    public Polynomial(String filename)throws IOException
    {
        String line;
        try(BufferedReader reader = new BufferedReader(new FileReader(filename)))
        {
            naive=exp=horner=fft = 0l;
            poly = new ArrayList<>();
            runTimes = new ArrayList<>();
            opCounts = new ArrayList<>();
            this.size = Integer.parseInt(reader.readLine());
            if(size < 1)
            {
                System.out.println("Number of polynomial terms must be a power of two.");
                System.exit(0);
            }
            String [] digits = new String[2];

            for(int i = 0; i < size; i++)
            {
                digits = reader.readLine().split(",");
                poly.add(new Complex(Double.parseDouble(digits[0]), Double.parseDouble(digits[1])));
            }
        }catch(FileNotFoundException fnfe)
        {
            throw new FileNotFoundException();
        }
    
    }
    public void naiveEval()
    {
       ops = 0;
       Complex result = new Complex(1,0);
       Complex coeff = new Complex(1, 0); 
       Complex nth = new Complex(1, 0);
       startTime = System.nanoTime();
       for(int i = 0; i < size; ++i)
       {          
           result = poly.get(0);
           nth = Complex.getNthRoot(i, size);
          for(int k = 1; k < size; ++k)
          {
              
              coeff = poly.get(k);
              Complex nthH = nth;
              for(int j = 1; j < k; ++j)
              {
                 nthH = nthH.multiply(nth); 
                 ops++;
              }
              ops++;
              result = Complex.addition(result, coeff.multiply(nthH));
          }
          //System.out.println("Naive: " + result.toString());
       }
       //System.out.println();   
       endTime = System.nanoTime();
       totalTime = endTime - startTime;
       System.out.println("Naive Run Time: " + (endTime - startTime)/1000000000.0);
       System.out.println("Number of Complex Multiplies: " + ops);
    }
    /**
     * Needs work.  Believe my values are backwards somehow.  
     * @return 
     */
    public void hornerEval()
    {
        ops = 0;
        startTime = System.nanoTime();
        for(int k = 0; k < size; ++k)
        {
            Complex result = new Complex(0,0);
            Complex nth = Complex.getNthRoot(k, size);
            for(int i = size-1; i >= 0; --i)
            {
                result = poly.get(i).addition(result.multiply(nth));
                ops++;
            }
            //System.out.println("Horners: " + result.toString());
        }
        endTime = System.nanoTime();
        totalTime = endTime - startTime;
        System.out.println("Horner's Run Time: " + (endTime - startTime)/1000000000.0);
        System.out.println("Number of Complex Multiplies: " + ops);   
    }

    public void fft()throws ArrayIndexOutOfBoundsException
    {
        ops = 0;
        startTime = System.nanoTime();
        Complex[] result = fftRec(poly.toArray(new Complex[size]));
        endTime = System.nanoTime();
        System.out.println("FFT Run Time: " + (endTime - startTime)/1000000000.0);
        System.out.println("Number of Complex Multiplies: " + ops);
        
    }
    
    private Complex[] fftRec(Complex[] vars)
    {
        int n = vars.length;
        if(n == 1)
        {
            return new Complex[]{vars[0]};
        }
        Complex [] even = new Complex[n / 2];
       // int count = 0;
        for(int i = 0; i < n/2; i++)
        {
            even[i] = vars[i*2];
        }
        //count = 0;
        Complex[] l = fftRec(even);
        Complex[] odd = new Complex[n/2];
        for(int i = 0; i < n/2; i++)
        {
            odd[i] = vars[i*2 + 1];
        }
        //count = 0;
        Complex[] r = fftRec(odd);
        
        Complex[] combine = new Complex[n];
        for(int y = 0; y < n/2; ++y)
        {
            Complex nth = Complex.getNthRoot(y, n);
            combine[y] = l[y].addition(nth.multiply(r[y]));
            ops++;
            combine[y + n/2] = l[y].subtract(nth.multiply(r[y])); 
            ops++;
        }
        return combine;
    }
    public void exponentiation()
    {
        ops = 0;
        startTime = System.nanoTime();
        for(int i = 0; i < size; i++)
        {
            Complex nth = Complex.getNthRoot(i, size);
            Complex result = new Complex(1, 1);
            result = poly.get(0);
            for(int j = 1; j < size; j++)
            {
                result = Complex.addition(poly.get(j).multiply(expo(nth, j)), result);
                ops++;
            }
            //ops++;
            //System.out.println(result.toString());
        }
        endTime = System.nanoTime();
        totalTime = endTime-startTime;
        System.out.println("Exponentiation Run Time: " + (endTime - startTime)/1000000000.0);
        System.out.println("Number of Complex Multiplies: " + ops);
    }
    
    private Complex expo(Complex comp, int n)
    {
        if(n == 0)
        {
            return  new Complex(1, 0);//This is equal to one
        }
        if(n == 1)
            return comp;
        
        Complex result = new Complex(0,0);
        
        if(n%2 == 0)
        {
         Complex rec = expo(comp, n/2);
         ops++;
         return Complex.multiply(rec, rec);
        }
        else
        {
         Complex rec = expo(comp, (n-1)/2);
         result = rec.multiply(rec);
         ops = ops + 1;
         return result.multiply(comp);
        }
    }
    public void displayCoefficients()
    {
        for(Complex c : poly)
        {
            System.out.print(c.toString() + " ");
        }
        System.out.println("\n");
        
    }
    
    public void writeFile(String filename) throws IOException
    {
        try(BufferedWriter bw = new BufferedWriter(new FileWriter(filename)))
        {
           
           bw.write(Integer.toString(poly.size()) + "\r\n"); 
           for(Complex c : poly)
           {
               bw.write(c.x + "," + c.y + "\r\n");
           }
        }catch(IOException ioe)
        {
            throw new IOException();
        }
    }
    public void timedRun(String filename)throws IOException
    {
        int[] times = new int[] {4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048};
        ArrayList<Long> time = new ArrayList<>();
        ArrayList<Long> count = new ArrayList<>();
        try(BufferedWriter bw = new BufferedWriter(new FileWriter(filename, true)))
        {
            PrintWriter out = new PrintWriter(bw);
                for(int i : times)
                {
                    System.out.println("====================================\nRunning with n = " + i);
                    out.write("n = " + i + " \n============================\r\n\n");

                   
                        poly = Complex.genRandom(i);
                        size = i;
                        naiveEval();
                        System.out.println("Naive finished.");
                        time.add(totalTime);
                        count.add(ops);
                        //out.write(Long.toString(totalTime) + ",");
                        //out.write(ops + " \r\n");
                        exponentiation();
                         time.add(totalTime);
                        count.add(ops);                       
                       // out.write(Long.toString(totalTime) + ",");
                        //out.write(ops + " \r\n");  
                        System.out.println("Exp finished.");
                        hornerEval();
                        time.add(totalTime);
                        count.add(ops);                        
                        //out.write(Long.toString(totalTime) + ",");
                       // out.write(ops + " \r\n");
                        System.out.println("Horner finished.");
                        fft();
                        time.add(totalTime);
                        count.add(ops);
                       // out.write(Long.toString(totalTime) + ",");
                        //out.write(ops + " \r\n");
                        System.out.println("FFT finished.");
                        for(int k = 0; k < time.size()-1; ++k)
                        {
                            out.write(time.get(k).toString() + ",");
                        }
                        out.write(time.get(time.size()-1).toString() + "\r\n");
      
                        for(int k = 0; k < count.size()-1; ++k)
                        {
                            out.write(count.get(k).toString() + ",");
                        }
                        out.write(count.get(count.size()-1).toString() + "\r\n");                       
                    
                }
        }catch(IOException ioe)
        {
           throw new IOException(); 
        }    
    }   
    
}
