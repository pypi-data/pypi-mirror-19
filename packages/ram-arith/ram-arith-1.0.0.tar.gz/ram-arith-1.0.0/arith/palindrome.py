def palindrome(a):
  b=reversed(a)
  if(list(a)==list(b)):
    print("palindrome")
  else:
    print("not palindrome")
