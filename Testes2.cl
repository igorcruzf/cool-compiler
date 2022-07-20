
(*
	c2i   Converts a 1-character string to an integer.  Aborts
	if the string is not "0" through "9"
*)

class A2I {

	c2i(char : String) : Int {
		if char = "0" then 0 else
		if char = "1" then 1 else
		if char = "2" then 2 else
		if char = "3" then 3 else
		if char = "4" then 4 else
		if char = "5" then 5 else
		if char = "6" then 6 else
		if char = "7" then 7 else
		if char = "8" then 8 else
		if char = "9" then 9 else{
			abort();
			0;
		}  -- the 0 is needed to satisfy the typchecker
			
		fi fi fi fi fi fi fi fi fi fi
	};
};
