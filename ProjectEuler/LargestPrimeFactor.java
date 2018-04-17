import java.lang.Math;

public class LargestPrimeFactor {

	public static void main (String[] args) {
		long value = 600851475143l;
		double square = Math.sqrt(value);
		long floor = (long)Math.floor(square);
		long answer = 0;
		//System.out.println(floor);
		for(int i = 2; i <= floor; i++) {
			//System.out.println(value%i);
			if(value % i == 0) {
			//System.out.println(i);

				if(isPrime(i))
				{
					answer = i;
				}
			}
		}
		System.out.println(answer);
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