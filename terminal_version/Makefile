CXX = g++
CXXFLAGS = -std=c++11 -O2 -Wextra -Wall -Wno-sign-compare -Wno-unused-result
FILES = main.cpp
NAME = solution

all: solution

solution:
	$(CXX) $(CXXFLAGS) -o $(NAME) $(FILES)

debug:
	$(CXX) $(CXXFLAGS) -o $(NAME) $(FILES) -g3

valgrind:
	valgrind --leak-check=full --show-leak-kinds=all --log-file=valgrind.txt ./$(NAME) < ./tests/test_01.txt

run:
	./$(NAME) < ./tests/test_01.txt
	./$(NAME) < ./tests/test_02.txt
	./$(NAME) < ./tests/test_03.txt
	./$(NAME) < ./tests/test_04.txt
	./$(NAME) < ./tests/test_05.txt
	./$(NAME) < ./tests/test_06.txt
	./$(NAME) < ./tests/test_07.txt
	./$(NAME) < ./tests/test_08.txt
	./$(NAME) < ./tests/test_09.txt
	./$(NAME) < ./tests/test_10.txt
	./$(NAME) < ./tests/test_11.txt
	./$(NAME) < ./tests/test_12.txt
	./$(NAME) < ./tests/test_13.txt
	./$(NAME) < ./tests/test_14.txt
	./$(NAME) < ./tests/test_15.txt
	./$(NAME) < ./tests/test_16.txt

clean:
	rm -f *.o $(NAME)