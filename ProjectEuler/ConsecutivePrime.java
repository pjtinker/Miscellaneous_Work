

public class ConsecutivePrime{

	public static void main(String[] args) {
		int target = 0;
		long index = 1;
		do {
			index++;
			if(isPrime(index)){
				System.out.println(index);
				target++;		
			}
		}while(target != 10001);
		System.out.println("target: " + target + " prime: " + index);
	}
	
	public static boolean isPrime(long x) {
		double s = Math.sqrt(x);
		long floor = (long)Math.floor(s);
		for(int k = 2; k <= s; ++k) {
			if(x % k == 0)
				return false;
		}
		return true;
	}
}