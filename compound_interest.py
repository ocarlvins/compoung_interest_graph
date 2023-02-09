from decimal import Decimal as d
import locale
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

def cell(item):
    try:
        return f'{item:,.2f}'.rjust(20)
    except Exception as e:
        return str(item).rjust(20)

def row(*args):
    print(''.join([cell(i) for i in args]))

class Investment:
    perc = d('10')
    deposit = d('0')
    interest = d('0')
    period = 0
    compounding = True

    points = []

    def __init__(self, perc, deposit, per=None, compounding=True) -> None:
        if perc:
            self.perc = d(perc)
        if deposit:
            self.deposit = deposit
        self.compounding = compounding

        self.per = d([1,12,365][per or 2])
        self.points = []
        pass

    def new_period(self, addition=d('0')):
        interest = self.deposit * self.perc/d(self.per)/d(100)
        self.interest += interest
        self.period += 1
        if self.compounding:
            self.deposit += interest + d(addition)
        else:
            self.deposit += d(addition)

        # self.points.append([d(f"{int(self.period/self.per)}.{(self.period%self.per)/self.per}"), self.deposit])
        self.points.append([self.period/self.per, self.deposit/d('1000000')])

        row(int(self.period/self.per), self.period%self.per, self.perc, self.interest, self.deposit)
        if self.compounding:
            return self.deposit
        else:
            return self.deposit + self.interest
        
    def get_points(self):
        return self.points

    def calculate(self):
        additions = []# [41000, 6000]

        for i in range(365*20):
            try:
                addition=additions[i]
            except Exception as e:
                addition=d('0')


            deposit = self.new_period(addition=addition)
            if deposit > (sum(additions) + initial)*2:
                break

periods = {
    'annually':0,
    'monthly': 1,
    'daily': 2
}

import matplotlib.pyplot as plt
import numpy as np
# li = list(zip(range(1, 14), range(14, 27)))

def linechart(*pairs):
    for num, pair in enumerate(pairs):
        axes = []
        axes.append([x[0] for x in pair])
        axes.append([x[1] for x in pair])
        plt.plot(*[np.array(i) for i in axes], ls=":", label=f"Pair {num}")

    plt.legend()
    plt.grid(color = 'green', linestyle = '--', linewidth = 0.5)
    plt.xlabel("Time in years")
    plt.ylabel("Deposits")
    plt.ylim(ymin=0)
    plt.xlim(xmin=0)
    plt.title('Correct Plot')
    plt.show()

initial = 20000000

mali  = Investment(d('7.7'), initial, periods['annually'], compounding=True)
mali.calculate()

mali2 = Investment(d('15'), initial, periods['annually'], compounding=True)
mali2.calculate()

linechart(
    mali.get_points(),
    mali2.get_points()
)

'''
                             Inferences
                       ---------------------

- Takes deposit of 20,000,000 to make 131,209 monthly interest if compounding daily at 7.7%
    if doing Safaricom Mali

Questions
    How long does it take to make 120,000 monthly?
    How long does it take to double the capital?

To Dos
    Create various models that will answer the questions above


Mansa X
    200 classes
    bonds and bills
    sydney
    asia
    europe
    kenya government 
    hedge fund 
        SIB
        Laurium Capital - South Africa

    5% fee
    gross 20.99%
    5% - finanial services chrge, management fees
    no tax on capital gains except real estate
    no joining
'''