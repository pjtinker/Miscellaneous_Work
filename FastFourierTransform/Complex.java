/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

import java.util.concurrent.ThreadLocalRandom;
import java.util.ArrayList;
import java.text.DecimalFormat;
/**
 *
 * @author hemlo
 */
public class Complex {
    public double x, y;
    private DecimalFormat fmt = new DecimalFormat("#.###");
    public Complex(double x, double y){
        this.x = x;
        this.y = y;
    }
    public double Real()
    {
        return x;
    }
    public double Imaginary()
    {
        return y;
    }
    public Complex addition(Complex a)
    {
        return new Complex(a.x + this.x, a.y + this.y);
    }
    public static Complex addition(Complex a, Complex b)
    {
        return new Complex(a.x + b.x, a.y + b.y);
    }
    public Complex multiply(Complex a)
    {
        return new Complex((x*a.x) - (y*a.y), (x * a.y) + (y * a.x));
    }
    public static Complex multiply(Complex a, Complex b)
    {
        return new Complex ((a.x * b.x) - (a.y*b.y), (a.x * b.y) + (a.y * b.x));
    }
    public Complex subtract(Complex a)
    {
        return new Complex(this.x - a.x, this.y - a.y);
    }
    public static ArrayList<Complex> genRandom(int n)
    {
        ArrayList<Complex> polynomial = new ArrayList<>();
        if(n > 0)
        {
            for(int i = 0; i < n; i++)
            {
                polynomial.add(new Complex(ThreadLocalRandom.current().nextInt(-10, 11), 0.0));
            }
        }
        
        return polynomial;
    }
    @Override
    public String toString()
    {
        
        if(y < 0)
            return "(" + fmt.format(x)  + " - " + fmt.format((-1*y)) + "i)";
        return "(" + fmt.format(x) + " + " + fmt.format(y) + "i)";
    }
    public static Complex getNthRoot(int k, int n)
    {
        double theta = (2.0 * (double)k * Math.PI) / (double)n; 
        return new Complex(Math.cos(theta), Math.sin(theta));
    }
    
    public static Complex getNthReg(int k, int n)
    {
        double theta = 2.0 * (double)k*Math.PI / (double) n;
        return new Complex(Math.cos(theta), Math.sin(theta));
    }
}
