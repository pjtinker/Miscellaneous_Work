/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */


/**
 *
 * @author hemlo
 */
public class ReinforcementLearner {

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args){

        if(args.length == 0 || args.length > 1)
        {
            System.out.println("Usage [filename]");
            System.exit(0);
        }
        States states = new States(args[0]);
        //states.valueIteration();
        states.reinforcementLearn(10000);
        System.out.println("Final Utilities:");
        states.displayUtils();
        System.out.println("Policy:");
        states.setPolicy();
        states.displayPolicy();
    }
    
}
