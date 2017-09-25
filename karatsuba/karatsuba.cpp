// coursera_algorithms.cpp : Defines the entry point for the console application.
//

#include "stdafx.h"
#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;
vector<int> karatsuba(vector<int>, vector<int>);
vector<int> operator+(const vector<int>&, const vector<int>&);
vector<int> operator-(const vector<int>&, const vector<int>&);
void pad(vector<int>&, vector<int>&);
void print_vect(vector<int>);
void strip(vector<int>&);

int main()
{
	vector<int> x = { 3,1,4,1,5,9,2,6,5,3,5,8,9,7,9,3,2,3,8,4,6,2,6,4,3,3,8,3,2,7,9,5,0,2,8,8,4,1,9,7,1,6,9,3,9,9,3,7,5,1,0,5,8,2,0,9,7,4,9,4,4,5,9,2 };
	vector<int> y = { 2,7,1,8,2,8,1,8,2,8,4,5,9,0,4,5,2,3,5,3,6,0,2,8,7,4,7,1,3,5,2,6,6,2,4,9,7,7,5,7,2,4,7,0,9,3,6,9,9,9,5,9,5,7,4,9,6,6,9,6,7,6,2,7 };
	//vector<int> x = { 1,0,2};
	//vector<int> y = { 2,3 };
	vector<int> result;
	result = karatsuba(x,y);
	print_vect(result);
    return 0;
}

vector<int> karatsuba(vector<int> x, vector<int> y) {
	//apply 0 padding to front if sizes are different
	pad(x, y);

	//base case: single-digit multiplication
	if (x.size() == 1 && y.size() == 1) {
		int product = x[0] * y[0];
		vector<int> v = { product / 10, product % 10 };
		strip(v);
		return v;
	}

	//splitting the inputs into two parts
	int div_mark = x.size() / 2;
	vector<int> a(x.begin(), x.begin() + div_mark);
	vector<int> b(x.begin() + div_mark, x.end());
	vector<int> c(y.begin(), y.begin() + div_mark);
	vector<int> d(y.begin() + div_mark, y.end());

	//computing products used in algorithm
	vector<int> ac = karatsuba(a, c);
	vector<int> bd = karatsuba(b, d);
	vector<int> mid = (karatsuba(a + b, c + d) - ac) - bd;

	//'multiply' by appropriate factors of 10
	vector<int> ac_pad((x.size() - div_mark) * 2, 0);
	vector<int> mid_pad(x.size() - div_mark, 0);
	ac.insert(ac.end(), ac_pad.begin(), ac_pad.end());
	mid.insert(mid.end(), mid_pad.begin(), mid_pad.end());

	return ac + mid + bd;
}

vector<int> operator+(const vector<int>& x, const vector<int>& y) {
	vector<int> temp;
	vector<int> a = x;
	vector<int> b = y;
	pad(a, b);

	int carry = 0;
	for (int i = 1; i <= a.size(); i++) {
		int sum = a[a.size() - i] + b[b.size() - i] + carry;
		temp.insert(temp.begin(), sum % 10);
		carry = sum / 10;
	}
	if (carry != 0) { temp.insert(temp.begin(), carry); }
	strip(temp);
	return temp;
}

vector<int> operator-(const vector<int>& x, const vector<int>& y) {
	vector<int> temp;
	vector<int> a = x;
	vector<int> b = y;
	pad(a, b);

	int borrow = 0;
	for (int i = 1; i <= a.size(); i++) {
		if (a[a.size() - i] < b[b.size() - i]) {
			if (int(a.size()) - i - 1 < 0) { throw invalid_argument("result must be >= 0"); }
			a[a.size() - i - 1] -= 1;
			borrow = 10;
		}
		int diff = a[a.size() - i] - b[b.size() - i] + borrow;
		temp.insert(temp.begin(), diff);
		borrow = 0;
	}
	strip(temp);
	return temp;
}

void pad(vector<int>& x, vector<int>& y) {
	if (x.size() != y.size()) {
		int diff = abs(int(x.size() - y.size()));
		vector<int> pad(diff, 0);
		if (x.size() < y.size()) {
			x.insert(x.begin(), pad.begin(), pad.end());
		}
		else {
			y.insert(y.begin(), pad.begin(), pad.end());
		}
	}
}

void print_vect(vector<int> x) {
	for (int i = 0; i < x.size(); i++) {
		cout << x[i];
	}
	cout << endl;
}

void strip(vector<int>& x) {
	while (x[0] == 0 && x.size() > 1) {
		x.erase(x.begin());
	}
}