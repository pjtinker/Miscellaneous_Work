/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

import java.lang.Math;
import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.concurrent.ThreadLocalRandom;

/**
 *
 * @author hemlo
 */
public class State {
    private double reward;
    private int actions, states;
    final public boolean terminal;
    public double utility;
    public double oldUtility;
    private Double[][] trueTransition;
    private Double[][] estTransition;
    private int[] actionTaken;
    private int[][] stateLanded;
    String policy;
    
    public State(String filename, double reward, boolean isTerminal){
        this.terminal = isTerminal;
        this.reward = reward;
        
        if(isTerminal)
        {
            utility = reward;
            oldUtility = reward;
            policy = "Finish";
        }else{
            utility = 0;   
        }
        String line;
        try(BufferedReader reader = new BufferedReader(new FileReader(filename)))
        {
            line = reader.readLine();
            String [] halvsies = line.split(" ");
            actions = Integer.parseInt(halvsies[0]);
            states = Integer.parseInt(halvsies[1]);
            trueTransition = new Double[actions][states];
            estTransition = new Double[actions][states];
            for(int i = 0; i < actions; i++){
                line = reader.readLine();
                String[] probs = line.split(" ");
                for(int k = 0; k < states; ++k){
                    trueTransition[i][k] = Double.parseDouble(probs[k]);
                    estTransition[i][k] = 0.0;
                }

            }   
            actionTaken = new int[]{1, 1, 1, 1};
            stateLanded = new int[actions][states];
          
        }catch(IOException ioe){

        }
    }
    public double getUtility(){
        return utility;
    }
    public double getReward(){
        return reward;
    }
    public double getTransProb(int action, int state){
        return trueTransition[action][state];
    }
    public void updateUtility(double newU)
    {
        oldUtility = utility;
        utility = newU;
    }
    public double getDifference()
    {
        //System.out.println("New util: " + utility + " Old util: " + oldUtility);
        double temp = utility - oldUtility;
        //System.out.println("Temp: " + temp);
        return Math.abs(temp); ///Should I have absolute value here?
    }
    public boolean isTerm()
    {
        return terminal;
    }
    public void updatePolicy(String pol){
        policy = pol;
    }
    public String getPolicy(){
        return policy;
    }
    public double getEstTrans(int action, int state){
        return estTransition[action][state];
    }
   public void incActionTaken(int a){
       actionTaken[a]++;
   } 
   public void incStateLanded(int a, int s){
       stateLanded[a][s]++;
   }
   
   public int makeMove(int moveSelection){
       double random = ThreadLocalRandom.current().nextDouble(0.0, 1.0);
       int  moveActual = 0;
       double culminate = 0.0;
       for(int i = 0; i < states; ++i)
       {
           culminate += trueTransition[moveSelection][i];
           if(random < culminate){
               moveActual = i;
               break; //break or continue?
           }
       }
       actionTaken[moveSelection]++;
       stateLanded[moveSelection][moveActual]++;
       //update the estimated probability table
       for(int i = 0; i < states; ++i){
           estTransition[moveSelection][i] = (double)stateLanded[moveSelection][i]/(double)actionTaken[moveSelection]; 
       }
       return moveActual;
   }
}
