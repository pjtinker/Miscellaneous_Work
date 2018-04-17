/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.concurrent.ThreadLocalRandom;
/**
 *
 * @author hemlo
 */
public class States {
    private ArrayList<State> states;
    private  int numActions, numStates;
    private  double gamma;
    
    public States(String filename){
        String line;
        states = new ArrayList<State>();
        try(BufferedReader reader = new BufferedReader(new FileReader(filename))){
            this.numActions = Integer.parseInt(reader.readLine());
            this.numStates = Integer.parseInt(reader.readLine());
            gamma = Double.parseDouble(reader.readLine());
            boolean truth;
            double reward;
            for(int i = 0; i < numStates; ++i){
                reward = Double.parseDouble(reader.readLine());
                
                if(Integer.parseInt(reader.readLine()) == 0){
                    truth = false;
                }else{
                    truth = true;
                }
                line = reader.readLine();
                //System.out.println("Sending file: " + line);
                states.add(new State(line, reward, truth ));
            }
            
        }catch(IOException ioe){
            System.out.println(ioe.getMessage());
        }   
    }   
    public void valueIteration(){
        double tol = 0.001;
        double diff = 100.0;
        double max = -1000.0;
        double temp = 0.0;
        double holder = 0.0;
        int counter = 0;
       
        do{
            for(int i = 0; i < numStates; ++i){
                State s = states.get(i);
                if(s.isTerm())
                    continue;
                max = -1000.0;
                for(int j = 0; j < numActions; ++j){
                     temp = 0.0;
                    for(int k = 0; k < numStates; ++k){
                      temp += s.getTransProb(j,k)*states.get(k).getUtility();
                    }
                       if(temp >= max)
                        max = temp;
                    
                }
              s.updateUtility(gamma*max + s.getReward());  
              diff = s.getDifference();
            }
        }while(diff > tol);
        //System.out.println(counter);
    }
    public void setPolicy()
{
    double max = 0.0;
    double prob = 0.0;
     for(int i = 0; i < numStates; ++i){
         State currentState = states.get(i);
        if(currentState.isTerm())
            continue;
        max = -1000.0;
        int action = 0; 
        for(int j = 0; j < numActions; ++j){
            double temp = 0.0;
            for(int k = 0; k < numStates; ++k){

              temp += currentState.getTransProb(j,k) * states.get(k).getUtility();
            }
               if(temp > max){
                   action = j;
                   max = temp;
               }       
               
        }
        
      currentState.updatePolicy(getMove(action));     
     }
    }
    public void displayUtils(){
        for(State s : states){
            System.out.println(s.getUtility());
        }
    }
    
    private String getMove(int index){
        
        String answer = "";
        switch(index){
            case(0): answer = "Up";
            break;
            case(1): answer = "Left";
            break;
            case(2): answer = "Down";
            break;
            case(3): answer = "Right";
            break;
            default: answer = "Unknown";
            break;
           }
            return answer;
        }
    public void displayPolicy(){
         for(State s : states){
            System.out.println(s.getPolicy());
        }       
    }

    public void reinforcementLearn(int count){
        for(int k = 0; k < count; k++){
            int random = ThreadLocalRandom.current().nextInt(0, 11);
            State currentState = states.get(random);
            do{
                int nextMove = 0;
                
                if(currentState.isTerm())
                    continue;
                double maxUtility = -1000.0;
                for(int i = 0; i < numActions; ++i){
                    double temp = 0.0;
                    for(int j = 0; j < numStates; ++j){
                        temp += currentState.getEstTrans(i, j) * states.get(j).getUtility();
                    }
                    if(temp > maxUtility){
                        maxUtility = temp;
                        nextMove = i;
                    }
                }
                currentState.updateUtility(gamma*maxUtility + currentState.getReward()); 
                currentState.updatePolicy(getMove(nextMove));
                if(ThreadLocalRandom.current().nextDouble(0.0, 1.0) < .10){
                    nextMove = ThreadLocalRandom.current().nextInt(0, 4);
                }
                currentState = states.get(currentState.makeMove(nextMove));   
                
                
            }while(!currentState.isTerm());
            if(k % 100 == 0)
            System.out.println("State " + random + " at iteration " + k + " utility: " + states.get(random).getUtility());
    }
    }
}
