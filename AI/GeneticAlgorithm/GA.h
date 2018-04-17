#if !defined GA_H
#define GA_H

#include <vector>
#include <algorithm>
#include <cstdlib>
#include <time.h>
#include <windows.h>
//#include <random>
using namespace std;

int myRandom(int i)
{
	return std::rand() % i;
}
class Chromosome {
	private:
		int fitness;
		vector<int> cities;
	public:
		Chromosome(vector<int> city_list, int** &matrix);
		int getFitness()
		{
			return fitness;
		}
		void printCities();
		bool operator ==(Chromosome other) const
		{
			return fitness == other.fitness;
		}
		bool operator <(Chromosome other) const
		{
			return fitness < other.fitness;
		}
		
		bool operator >(Chromosome other) const
		{
			return fitness > other.fitness;
		}
		void generateFitness(int** &mat);
		int getSize(){return cities.size();}
		vector<int> getCities()
		{
			return cities;
		}
		void setCities(vector<int> ncities){cities = ncities;}
};
class Population {
	private:
		vector<Chromosome> chroms;
		int fittest_gene;
	public:
		Population(vector<Chromosome> input)
		{chroms = input;}
		Chromosome getChrom(int index){return chroms[index];}
		void nextGen(int** &matrix, int num_gens, int num_pop);
		void crossover(Chromosome &one, Chromosome &two, int** &matrix);
		bool operator <(Population other) const
		{
				return chroms[chroms.size()-1] < other.chroms[other.chroms.size()-1];
		}
		Chromosome getFittestChrom(){return chroms[0];}
};
void shuffle(vector<int> &cit)
{
	random_shuffle(cit.begin()+1, cit.end()-1, myRandom);	//leave first and last alone
	
}
void Population::nextGen(int** &matrix, int num_gens, int num_pop)
{	
	vector<Chromosome> rand_mutes;
	vector<Chromosome> choices;
	vector<Chromosome> next;
	vector<Population> results;
	int first_r = 0;
	int sec_r = 0;
	int count = 10;
	
	for(int i = 0; i < num_gens; ++i)
	{
		sort(chroms.begin(), chroms.end());
		for(int k = 0; k < 10; ++k)
		{
			next.push_back(chroms[k]);
		}
		for(; count < num_pop; count += 2)
		{	
			for(int l = 0; l < 10; ++l)
			{
				rand_mutes.push_back(chroms[myRandom(chroms.size())]);
			}
			sort(rand_mutes.begin(), rand_mutes.end());

			do
			{
				first_r = myRandom(4);
				sec_r = myRandom(4);
			}while(first_r == sec_r);
			
			choices.push_back(rand_mutes[first_r]);
			choices.push_back(rand_mutes[sec_r]);
			crossover(choices[0], choices[1], matrix);

			next.insert(next.end(), choices.begin(), choices.end());
			rand_mutes.clear();
			choices.clear();

		}

		count = 10;
		chroms = next;
		next.clear();
	}

	
}
void Population::crossover(Chromosome &one, Chromosome &two, int** &matrix)
{

	vector<int> missing;
	vector<int> rep;
	vector<int> none = one.getCities();
	vector<int> ntwo = two.getCities();
	rep.assign(none.size(), 0);
	vector<int> dup;
	
	int crosspoint = rand()%(none.size()); 
	if(crosspoint >= 15)
	{
		crosspoint = 14;
	}
	if(crosspoint == 0)
		crosspoint++;

	int random = rand()%100 + 1;
	
	if(random < 15) //This mutation step improves convergence
	{
		reverse(none.begin(), none.end());
	}
	
	swap_ranges(ntwo.begin(), ntwo.begin() + crosspoint, none.begin());

	for(unsigned int i = 1; i < none.size()-1; ++i)
	{

		if(rep[none[i]] == 0) //if value at represented at none's index equals 0, then we haven't seen that value yet
		{
			rep[none[i]]++;//we increment once we have seen it
			
		}else{ //we have seen this index once before, so it is a duplicate.  
			dup.push_back(i); //the value added to dupe is the index of the duplicate 
		}
	}
	for(unsigned int i = 1; i < rep.size()-1; ++i)  //traverse represented.  If any values are 0, then we missed that location.  
	{
		if(rep[i] == 0)
		{
			missing.push_back(i);
		}
	}
	
	for(int i = dup.size()-1; i >= 0; --i)
	{

		crosspoint = rand() % missing.size();
		none[dup[i]] = missing[crosspoint];
		missing.erase(missing.begin() + crosspoint);
		
	}
	rep.clear();
	rep.assign(ntwo.size(), 0);
	missing.clear();
	dup.clear();
	for(unsigned int i = 1; i < ntwo.size()-1; ++i)
	{
		if(rep[ntwo[i]] == 0) //if value at represented at ntwo's index equals 0, then we haven't seen that value yet
		{
			rep[ntwo[i]]++;//we increment once we have seen it
			
		}else{ //we have seen this index once before, so it is a duplicate.  

			dup.push_back(i); //this index will be the index of the value in ntwo where the duplicate is located.
		}
	}
	for(unsigned int i = 1; i < rep.size()-1; ++i)  //traverse represented.  If any values are 0, then we missed that location.  
	{
		if(rep[i] == 0)
		{
			missing.push_back(i);
		}
	}
	
	for(int i = dup.size()-1; i >= 0; --i)//randomly select missing value to replace duplicates
	{
		crosspoint = rand() % missing.size();
		ntwo[dup[i]] = missing[crosspoint];
		missing.erase(missing.begin() + crosspoint);
	}
	one.setCities(none);//reset city vectors
	two.setCities(ntwo);
	one.generateFitness(matrix);//generate new fitness 
	two.generateFitness(matrix);
	
}
Chromosome::Chromosome(vector<int> city_list, int** &matrix)
{
	cities = city_list;
	generateFitness(matrix);

}
void Chromosome::printCities()
{
	
	for(vector<int>::iterator it=cities.begin()+1; it != cities.end()-1; ++it)
	{
		cout << *it << " ";
	}
	cout << endl;
}

void Chromosome::generateFitness(int** &matrix) 
{
	fitness = 0;
	for(unsigned int i  = 0; i < cities.size()-1;)
	{
		fitness += matrix[cities[i++]][cities[i]];
	}
	
}


#endif