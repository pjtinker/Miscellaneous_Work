

public class LargestPalindrome {

	public static void main(String[] args) {
		int largestPali = 0;
		for(int i = 999; i > 0; --i) {
			for(int k = 999; k > 0; --k) {
				if(isPalindrome(k*i)) {
					//System.out.println("k: " + k + " i: " + i);
					if(largestPali < k*i)
						largestPali = k*i;
				}
					
			}
		}
		System.out.println(largestPali);
	}
	
	public static boolean isPalindrome(int value) {
		String number = Integer.toString(value);
		//System.out.println(number);
		int len = number.length()-1;
		for(int i = 0; i <= len/2; ++i) {
			if(number.charAt(i) != number.charAt(len - i))
				return false;
		}
		return true;
	}
}