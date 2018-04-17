	for(int i = 0; i < num_gens; ++i)
	{
		cout << "beginning generation " << gen_count++ << endl;
		sort(chroms.begin(), chroms.end());
		for(unsigned int j =0; j < chroms.size(); ++j)
		{
			cout << "cities at chrom " << j << " ";
			chroms[j].printCities();
		}
		for(unsigned int k = chroms.size()-1; k > chroms.size()-11; --k)
		{
			//cout << "top ten chroms: " <<  chroms[k].getFitness() << endl;
			//cout << "top ten chroms cities at index : " << k << ": ";
		    //chroms[k].printCities();

			next.push_back(chroms[k]);
		}
		for(; count < num_pop; count +=10)
		{
			for(int l = 0; l < 10; ++l)
			{
				random = rand() % chroms.size();
				cout << "random number " << random << endl;
				rand_mutes.push_back(chroms[random]);
				cout << "chroms added to random mutes: " << chroms[random].getFitness() << endl;
			}
			//cout << rand_mutes.size() << endl;
			sort(rand_mutes.begin(), rand_mutes.end());
			do
			{
				first_r = rand() % 4;
				sec_r = rand() % 4;
				//cout << first_r << " " << sec_r << endl;
			}while(first_r == sec_r);
			//cout << "fitness before " << endl;
			//cout << rand_mutes[6 + first_r].getFitness() << endl;
			//cout << rand_mutes[6 + sec_r].getFitness() << endl;
			crossover(rand_mutes[6 + first_r], rand_mutes[6 + sec_r], matrix);
			//cout << "fitness after " << endl;
			//cout << rand_mutes[6 + first_r].getFitness() << endl;
			//cout << rand_mutes[6 + sec_r].getFitness() << endl;
			next.insert(next.end(), rand_mutes.begin(), rand_mutes.end());
			//cout << "next size after random mutes: " << next.size() << endl;
			rand_mutes.clear();
			sort(next.begin(), next.end());
			/*for(unsigned int l = 0; l < next.size(); ++l)
			{
				cout << "next array fitness: " << next[l].getFitness() << endl;
			}
			cout << endl;*/
			//cout << "next size is " << next.size() << endl;
		}
		//sort(next.begin(), next.end());
		count = 10;
		chroms.clear();
		chroms = next;
		next.clear();
	}
	sort(chroms.begin(), chroms.end());
	cout << "chroms size: " << chroms.size() << endl;
	cout << chroms[chroms.size()-1].getFitness() << " ";
	chroms[chroms.size()-1].printCities();
	
}
void Population::crossover(Chromosome &one, Chromosome &two, int** &matrix)
{
	//Dont forget to generate fitness for the new chroms
	vector<int> rep;
	rep.assign(one.getSize(), 0);
	vector<int> dup;
	int crosspoint = rand()%one.getSize(); //These may not be random enough
	if(crosspoint >= 15)
	{
		crosspoint = 14;
	}
	int random = 0;
	//cout << "crosspoint " << crosspoint << endl;
	//cout << "one fitness: " << one.getFitness() << endl;
	//cout << "two fitness: " << two.getFitness() << endl;
	//one.printCities();
	//two.printCities();
	//cout << endl;
	swap_ranges(one.getCities().begin()+1, one.getCities().begin()+1+crosspoint, two.getCities().begin()+1);

	
	for(unsigned int i = 1; i < one.getCities().size()-1; ++i)
	{
		
		if(rep[one.getCities()[i]] == 0)
		{
			rep[one.getCities()[i]]++;
		}else
		{
			dup.push_back(i);
		}
	}
	/*if(dup.size() > 2)  //do i need to make this shuffle for 2 items?
	{
		shuffle(dup);
	}else if(dup.size() == 2)
	{
		random = dup[0];
		dup[0] = dup[1];
		dup[1] = random;
		random = 0;

	}*/
	for(unsigned int i = 1; i < one.getCities().size()-1; ++i)
	{
		if(rep[i] == 0)
		{
			one.getCities()[dup[random++]] = i;
		}
	}
	one.generateFitness(matrix);
	//cout << "one new fitness: " << one.getFitness() << endl;
	random = 0;
	dup.clear();
	rep.clear();
	rep.assign(one.getSize(), 0);
	for(unsigned int i = 1; i < two.getCities().size()-1; ++i)
	{
		
		if(rep[two.getCities()[i]] == 0)
		{
			rep[two.getCities()[i]]++;
		}else
		{
			dup.push_back(i);
		}
	}
	/*if(dup.size() > 2)
	{
		cout << "inside shuffle" << endl;
		//shuffle(dup);
	}else if(dup.size() == 2)
	{
		cout << "inside if dupe size two" << endl;
		random = dup[0];
		dup[0] = dup[1];
		dup[1] = random;
		random = 0;

	}*/
	for(unsigned int i = 1; i < two.getCities().size()-1; ++i)
	{
		if(rep[i] == 0)
		{
			two.getCities()[dup[random++]] = i;
		}
	}
	two.generateFitness(matrix);
	//cout << "two new fitness: " <<  two.getFitness() << endl;
	//one.printCities();
	//two.printCities();
	//cout << endl;
}