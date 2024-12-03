import math

def Calculate_interest():
    while True:
        initial = input("What is the full cost of the potential loan: $")
        try:
            initial = float(initial)
            if initial < 0:
                print("Please enter a positive number.")
                continue
            break
        except ValueError:
            print("Sorry, please enter a valid number.")
    
    loanType = "compound"
    
    while True:
        try:
            interestRate = float(input("Interest rate (as a percentage)? ")) / 100
            if interestRate < 0:
                print("Please enter a positive interest rate.")
                continue
            break
        except ValueError:
            print("Sorry, please enter a valid number.")
    
    while True:
        try:
            payment = float(input("How much are you planning to pay monthly? "))
            if payment <= 0:
                print("Please enter a positive payment amount.")
                continue
            break
        except ValueError:
            print("Sorry, please enter a valid number.")

    # Calculate time to pay off the loan
    if loanType == "simple":
        pass
        # time_to_payoff, total_paid = Calculate_simple_interest(initial, interestRate, payment)
    if loanType == "compound":
        time_to_payoff, total_paid, balances, interests = Calculate_compound_interest(initial, interestRate, payment)
    else:
        print("Invalid loan type.")
        return

    print(f"Initial Loan Amount: ${initial:.2f}, Loan Type: {loanType}, Interest Rate: {interestRate * 100:.2f}%, Monthly Payment: ${payment:.2f}")
    print(f"Time to pay off the loan: {time_to_payoff:.2f} months")
    
    # Compare with saving to buy outright
    time_to_save = initial / payment
    print(f"Time to save enough to buy outright: {time_to_save:.2f} months")
    
    # Calculate total savings
    savings = total_paid - initial
    print(f"Total amount spent on the loan: ${total_paid:.2f}")
    print(f"Amount saved by not paying interest: ${savings:.2f}")

    time_to_save = initial / payment
    # visualization.plot_time_comparison(initial, time_to_payoff, time_to_save, payment, interestRate)

def Calculate_compound_interest(amount, rate, payment):
    """Calculate compound interest details."""
    months = 0
    total_paid = 0
    balances = []  # Track loan balances over time
    interests = []  # Track interest paid over time

    while amount > 0:
        # Calculate interest for the current month
        interest = amount * rate / 12  # Monthly interest

        # Check if payment is sufficient to cover interest
        if payment <= interest:
            raise ValueError("Monthly payment is too low to cover the interest. Loan cannot be repaid.")

        # Deduct payment from the principal after paying interest
        principal_payment = payment - interest
        amount -= principal_payment

        # Handle final month if payment exceeds remaining balance
        if amount < 0:
            payment += amount  # Adjust the last payment
            principal_payment += amount  # Reduce principal payment
            amount = 0  # Set balance to zero

        # Update totals and logs
        total_paid += payment
        months += 1
        balances.append(max(amount, 0))  # Ensure non-negative balance
        interests.append(interest)

    return months, total_paid, balances, interests
