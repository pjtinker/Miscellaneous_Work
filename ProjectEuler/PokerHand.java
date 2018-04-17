
import java.io.BufferedReader;
import java.io.FileReader;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.util.ArrayList;
import java.lang.Math;
public class PokerHand implements Comparable<PokerHand>{
		public int highCard;
		
		public ArrayList<Integer> hearts;
		public ArrayList<Integer> clubs;
		public ArrayList<Integer> spades;
		public ArrayList<Integer> diamonds;
		public int numHearts;
		public int numClubs;
		public int numSpades;
		public int numDiamonds;
		public String[] cards;
		
	public static void main(String[] args) {
		try{
		BufferedReader br = new BufferedReader(new FileReader("poker.txt"));
		int numWins = 0;
		String line;
			while((line = br.readLine()) != null){
				//System.out.println(line.substring(0, 14));
				//System.out.println(line.substring(15));
				PokerHand one = new PokerHand(line.substring(0, 14));
				PokerHand two = new PokerHand(line.substring(15));
				int result = one.compareTo(two);
				//System.out.println(one.numSpades);
				if(result > 0)
					numWins++;
			}
			br.close();
		}catch(IOException ex) {
			System.out.println(ex.getMessage());
		}
		
	}
	
	public PokerHand(String deets){

		String[] cards = deets.split(" ");
		hearts = new ArrayList<>();
		clubs = new ArrayList<>();
		spades = new ArrayList<>();
		diamonds = new ArrayList<>();
		numClubs = 0;
		numHearts=0;
		numDiamonds=0;
		numSpades=0;
		int card = 0;
		int highCard = 0;
		for(String s : cards) {
			char suit = s.charAt(1);
			char value = s.charAt(0);
			
			if(!Character.isDigit(value)) {
				card = getValue(value);
			}else{
				card = Integer.parseInt(String.valueOf(value));
			}
			//System.out.println("Card: " + card);
			if(card > highCard)
				highCard = card;
			assignCard(card, suit);
		}
		
	}
	
	public int compareTo(PokerHand other) {
		int numOne = evaluate(this);
		int numTwo = evaluate(other);
		if(numOne > numTwo)
		{
			return 1;
		}else if(numOne < numTwo){
			return -1;
		}else{return 0;}	
	}
	private boolean isRoyalFlush(PokerHand ph) {
		return true;
	}
	private int getValue(char c) {
		int value = 0;
		//System.out.println("C: " + c);
		switch(c){
			case 'T': 
					value = 10;
					break;
			case 'K': 
					value = 13;
					break;
			case 'J':
					value = 11;
					break;
			case 'Q':
					value = 12;
					break;
			case 'A':
					value = 14;
					break;
		}
		return value;
	}
	private void assignCard(int value, char suit) {
		switch(suit){
			case 'D':
					diamonds.add(value);
					numDiamonds++;
					break;
			case 'S':
					spades.add(value);
					numSpades++;
					break;
			case 'C':
					clubs.add(value);
					numClubs++;
					break;
			case 'H':
					hearts.add(value);
					numHearts++;
					break;
			
		}
	}
	public int highestNumSuit() {
		return Math.max(numHearts, Math.max(numClubs, Math.max(numSpades, numDiamonds)));
	}

}
