#   Basic grading systems with letter output
# so above 50 marks its pass or P, below 50 Fail of F, 51-60 its E, 61-70 its D, 71-80 its C and 81-90 its B and 91-100 its A 

marks = int(input("Enter the marks: "))
if marks < 50:
    print("FAIL: grade F")
elif marks > 50 and marks <= 60:
    print(" PASS: grade E")
elif marks > 60 and marks <= 70:
    print(" PASS: grade D")
elif marks >70 and marks <= 80:
    print(" PASS: grade C")
elif marks >80 and marks <= 90:
    print(" PASS: grade B")
elif marks >90 and marks <= 100:
    print(" PASS: grade A")
else:
    print(" INVALID MARKS ")