from otree.api import (
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    Currency as c,
    currency_range,
)
import random

author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'mm2'
    players_per_group = None
    tasks = ['TOU', 'RTP', 'PET', 'AUC']
    num_rounds = len(tasks)+1

    example_player_vardemand = [3, 7]
    example_competition_vardemand = [1, 5]
    example_res = [5, 8]
    example_prices_tou = [2.0, 3.5]
    example_competition_bid_pet = 3.5
    example_competition_bid_auc = [3.5, 4.0]

    player_vardemand_rtp = [[2, 6], [3, 6]]
    competition_vardemand_rtp = [[4, 7], [6, 10]]
    res_rtp = [[3, 16], [12, 13]]

    player_vardemand_tou = [[3, 6], [4, 6]]
    competition_vardemand_tou = [[2, 7], [4, 8]]
    res_tou = [[8, 10], [5, 17]]
    prices_tou = [[2.0, 3.5], [2.0, 3.5]]

    player_vardemand_pet = [[2, 5], [3, 6]]
    competition_vardemand_pet = [[2, 6], [2, 6]]
    competition_bid_pet = 3.0
    res_pet = [[7, 8], [2, 15]]

    player_vardemand_auc = [[3, 4], [1, 6]]
    competition_vardemand_auc = [[2, 7], [3, 6]]
    competition_bid_auc = [[2.0, 4.0], [2.0, 4.0]]
    res_auc = [[2, 14], [7, 9]]

    def calculateRTP(self, q):
        p = 0
        if q < 0.5:
            p = 5.0
        elif q < 0.9:
            p = 4.0
        elif q < 1.1:
            p = 3.0
        elif q < 1.5:
            p = 2.0
        elif q >= 1.5:
            p = 1.0

        return p

    def determineOverdemand(self, first, demand, compDemand, renewables):
        overdemand = 0
        if first:
            if demand>renewables:
                overdemand = demand-renewables
            else:
                overdemand = 0
        else:
            if compDemand>=renewables:
                overdemand = demand
            elif compDemand + demand > renewables:
                overdemand = demand - (renewables-compDemand)
            else:
                overdemand = 0

        return overdemand

class Subsession(BaseSubsession):
    def creating_session(self):
        if self.round_number == 1:
            for p in self.get_players():
                round_numbers = list(range(1, Constants.num_rounds))
                random.shuffle(round_numbers)
                p.participant.vars['task_rounds'] = dict(zip(Constants.tasks, round_numbers))

    pass

class Group(BaseGroup):
    pass

class Player(BasePlayer):

    # Input Users
    Spiel_Counter = models.IntegerField()
    game_played = models.StringField()

    R1_P1_player_vardemand = models.FloatField(min=0, label='')
    R1_P2_player_vardemand = models.FloatField(min=0, label='')
    R2_P1_player_vardemand = models.FloatField(min=0, label='')
    R2_P2_player_vardemand = models.FloatField(min=0, label='')

    example_P1_vardemand = models.FloatField(min=0, label='')
    example_P2_vardemand = models.FloatField(min=0, label='')


    R1_P1_player_bid_auc = models.FloatField(label='', min=1, max=5.0, initial=3.0)
    R1_P2_player_bid_auc = models.FloatField(label='', min=1, max=5.0, initial=3.0)

    example_P1_player_bid_auc = models.FloatField(label='', min=1, max=5.0, initial=3.0)
    example_P2_player_bid_auc = models.FloatField(label='', min=1, max=5.0, initial=3.0)

    R2_P1_player_bid_auc = models.FloatField(label='', min=1, max=5.0, initial=3.0)
    R2_P2_player_bid_auc = models.FloatField(label='', min=1, max=5.0, initial=3.0)

    Rx_player_bid_pet = models.FloatField(label='', min=1, max=5.0, initial=3.0)

    example_player_bid_pet = models.FloatField(label='', min=1, max=5.0, initial=3.0)

    # Recording from Games
    total_adjustment_cost = models.FloatField(initial=0)

    ERWIRTSCHAFTET = models.FloatField(initial=0)

    total_cost_with_adjustment_cost = models.FloatField(initial=0)
    verguetung = models.FloatField(initial=0)

    adjustment_cost_example = models.FloatField(initial=0)
    total_cost_example = models.FloatField(initial=0)

    prolificID = models.LongStringField(
        label="Please enter your Prolific ID.",
        initial='',
        blank=True
    )

    Choice = models.StringField(
        label="",
        choices=[
            ['TOU',
             'Time of Use Pricing: Energy prices are externally set by the operator for all days equally in advance. They do not change based on your demand.'],
            ['RTP',
             'Real Time Pricing: Energy prices are externally set by the operator for every period individually. If you move your demand from or to the afternoon period, this might impact the price.'],
            ['PET',
             'Periodic Tariff: You can bid what you are willing to pay for energy once. You can then consume renewable energy for that price but renewable energy is distributed according to the ranking of the bids between you and the competition. Non-renewable energy costs 5.0 monetary units.'],
            ['AUC',
             'Auction Tariff: You can bid what you are willing to pay for energy for every period individually. You can then consume renewable energy for that price but renewable energy is distributed according to the ranking of the bids between you and the competition. Non-renewable energy costs 5.0 monetary units.'],
        ],
        widget=widgets.RadioSelect,
    )
    Choice2 = models.StringField(
        label="",
        choices=[
            ['TOU',
             'Time of Use Pricing: Energy prices are externally set by the operator for all days equally in advance. They do not change based on your demand.'],
            ['RTP',
             'Real Time Pricing: Energy prices are externally set by the operator for every period individually. If you move your demand from or to the afternoon period, this might impact the price.'],
            ['PET',
             'Periodic Tariff: You can bid what you are willing to pay for energy once. You can then consume renewable energy for that price but renewable energy is distributed according to the ranking of the bids between you and the competition. Non-renewable energy costs 5.0 monetary units.'],
            ['AUC',
             'Auction Tariff: You can bid what you are willing to pay for energy for every period individually. You can then consume renewable energy for that price but renewable energy is distributed according to the ranking of the bids between you and the competition. Non-renewable energy costs 5.0 monetary units.'],
        ],
        widget=widgets.RadioSelect,
    )

    Quiz1 = models.IntegerField(
        label="",
        choices=[
            [1,'The supply of renewables is always equal'],
            [2,'On the third day of every electricity rate design '],
            [3,'In the second electricity rate design'],
            [4,'In the afternoon'],
        ],
        widget=widgets.RadioSelect,
    )

    Quiz2 = models.IntegerField(
        label="",
        choices=[
            [1,'I can move my demand between different electricity rate designs. It only matters that at the end of the experiment, I have consumed the specified amount. '],
            [2, 'I can move my demand between morning and afternoon within one day.'],
            [3, 'I can deliberately choose how much energy to consume.'],
            [4, 'I can move my demand between days.'],
        ],
        widget=widgets.RadioSelect,
    )

    Quiz3 = models.IntegerField(
        label="",
        choices=[
            [1,
             '4 electricity rate designs, 3 days each and every day consists of morning, afternoon and evening'],
            [2, '2 electricity rate designs, 2 days each and every day consists of morning and afternoon'],
            [3, '4 electricity rate designs, 2 days each and every day consists of morning and afternoon'],
            [4, '6 electricity rate designs, 1 day each and every day consists of afternoon and evening'],
        ],
        widget=widgets.RadioSelect,
    )

    WrongAnswer1 = models.StringField
    WrongAnswer2 = models.StringField
    WrongAnswer3 = models.StringField

    Komplex = models.IntegerField(
        label="I found it a complex task to handle this electricity rate design.",
        choices=[
            [1, ''],
            [2, ''],
            [3, ''],
            [4, ''],
            [5, ''],
            [6, ''],
            [7, ''],
        ],
        widget=widgets.RadioSelectHorizontal,
    )

    Anspruchsvoll = models.IntegerField(
        label="It was mentally demanding engaging with this electricity rate design.",
        choices=[
            [1, ''],
            [2, ''],
            [3, ''],
            [4, ''],
            [5, ''],
            [6, ''],
            [7, ''],
        ],
        widget=widgets.RadioSelectHorizontal,
    )
    Denkvermoegen = models.IntegerField(
        label="Dealing with this electricity rate design required a lot of thought and problem-solving.",
        choices=[
            [1, ''],
            [2, ''],
            [3, ''],
            [4, ''],
            [5, ''],
            [6, ''],
            [7, ''],
        ],
        widget=widgets.RadioSelectHorizontal,
    )

    TOU_Attention = models.IntegerField(
        label="Please select option 4-I'm indifferent, right in the middle of the spectrum.",
        choices=[
            [1, ''],
            [2, ''],
            [3, ''],
            [4, ''],
            [5, ''],
            [6, ''],
            [7, ''],
        ],
        widget=widgets.RadioSelectHorizontal,
    )

    PET_Attention = models.IntegerField(
        label="Please select option 1-Completely dissatisfied, the left-most option.",
        choices=[
            [1, ''],
            [2, ''],
            [3, ''],
            [4, ''],
            [5, ''],
            [6, ''],
            [7, ''],
        ],
        widget=widgets.RadioSelectHorizontal,
    )

    Herausfordernd = models.IntegerField(
        label="I found this electricity rate design challenging to manage.",
        choices=[
            [1, ''],
            [2, ''],
            [3, ''],
            [4, ''],
            [5, ''],
            [6, ''],
            [7, ''],
        ],
        widget=widgets.RadioSelectHorizontal,
    )

    Zufrieden = models.IntegerField(
        label="How happy are you with the result?",
        choices=[
            [1, ''],
            [2, ''],
            [3, ''],
            [4, ''],
            [5, ''],
            [6, ''],
            [7, ''],
        ],
        widget=widgets.RadioSelectHorizontal,
    )

    Risikobereitschaft = models.IntegerField(
        label="",
        choices=[
            [1, ''],
            [2, ''],
            [3, ''],
            [4, ''],
            [5, ''],
            [6, ''],
            [7, ''],
        ],
        widget=widgets.RadioSelectHorizontal,
    )

    Geschlecht = models.StringField(
        label="Gender",
        choices=["Female", "Male", "Diverse", "I don't identify with any of the given options"]
    )
    Alter = models.StringField(
        label="Age",
        choices=["Below 18 years", "18-24", "25-29", "30-39", "40-49", "50-59",
                 "60-69", "70-79", "80 years or older"]
    )
    Hoechste_berufliche_Qualifikation = models.StringField(
        label="Highest level of qualification",
        choices=["No qualification", "Professional qualification", "Bachelor's degree",
                 "Master's degree", "Doctorate"]
    )
    Erwerbsstatus = models.StringField(
        label="Occupation",
        choices=["Employed", "Self-employed", "Currently unemployed",
                 "Retired", "Student", "Other"]
    )
    Einkommen = models.StringField(
        label="Average monthly household income",
        choices=["Below 1000 GBP", "1000-2000 GBP", "2000-3000 GBP",
                 "3000-4000 GBP", "Over 4000 GBP", "Don't know/don't want to say"]
    )

    FinalFeedback = models.LongStringField(
        label="Do you have any final remarks?",
        initial='',
        blank=True
    )

    Feedback = models.LongStringField(
        label="",
        initial='',
        blank=True
    )

    START_time_epoch = models.FloatField()
    ENDE_time_epoch = models.FloatField()

    def set_initial_num_participants(self):
        if self.test_existance_of_session_vars() == False:
            self.session.vars['num_participants_finished'] = 0

    def test_existance_of_session_vars(self):
        check = False
        if 'num_participants_finished' in self.session.vars:
            check = True
        return check


    player_id = models.StringField()

    pass