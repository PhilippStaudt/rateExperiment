from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants as Constants
import random
import time

class Full(Page):
    def is_displayed(self):

        displayed = False

        if self.player.test_existance_of_session_vars() == True:
            if self.session.vars['num_participants_finished'] >= 5000:
                displayed = True
        return (displayed and self.round_number == 1)

class Erklaerung1(Page):
    def is_displayed(self):
        return self.round_number == 1 and (self.player.field_maybe_none('Quiz1') != 4 or self.player.field_maybe_none('Quiz2') != 2 or self.player.field_maybe_none('Quiz3') != 3)
    def vars_for_template(self):

        if (self.player.field_maybe_none('Quiz1') == 4 or self.player.field_maybe_none('Quiz1') == None) and (self.player.field_maybe_none('Quiz2') == 2 or self.player.field_maybe_none('Quiz2') == None) and (self.player.field_maybe_none('Quiz3') == 3 or self.player.field_maybe_none('Quiz3') == None):
            self.player.WrongAnswer3 = ' '
        else:
            self.player.WrongAnswer3 = 'At least one of your answers was incorrect. You have therefore been redirected to the introductory pages. Please read the instruction carefully. You have one remaining attempt to answer the questions correctly.'

        return {
            "WrongAnswer3": self.player.WrongAnswer3,
        }

class Erklaerung2(Page):

    def is_displayed(self):
        return self.round_number == 1 and (self.player.field_maybe_none('Quiz1') != 4 or self.player.field_maybe_none('Quiz2') != 2 or self.player.field_maybe_none('Quiz3') != 3)
    def vars_for_template(self):

        return {

            "E_P1_player_vardemand": 3,
            "E_P2_player_vardemand": 7,
            "E_P1_competition_vardemand": 1,
            "E_P2_competition_vardemand": 5,
            "E_P1_supply_res": 5,
            "E_P2_supply_res": 8,

        }

class ErklaerungConsent(Page):
    form_model = 'player'
    form_fields = ["prolificID"]
    def is_displayed(self):
        return self.round_number == 1
    def vars_for_template(self):
        self.player.START_time_epoch = time.time()

    def before_next_page(self):
        self.player.set_initial_num_participants()

class Quiz(Page):
    form_model = 'player'
    form_fields = ["Quiz1", "Quiz2", "Quiz3"]
    def is_displayed(self):
        return self.round_number == 1 and (self.player.field_maybe_none('Quiz1') != 4 or self.player.field_maybe_none('Quiz2') != 2 or self.player.field_maybe_none('Quiz3') != 3)

class Quiz1_Falsch(Page):
    form_model = 'player'
    form_fields = ["Quiz1"]
    def is_displayed(self):
        return self.round_number == 1

class Quiz2(Page):
    form_model = 'player'
    form_fields = ["Quiz2"]
    def is_displayed(self):
        return self.round_number == 1

class Wahl(Page):
    form_model = 'player'
    form_fields = ["Choice"]
    def is_displayed(self):
        return self.round_number == 5

    def vars_for_template(self):
        return{
            "tou": self.participant.vars['task_rounds']['TOU'],
            "rtp": self.participant.vars['task_rounds']['RTP'],
            "pet": self.participant.vars['task_rounds']['PET'],
            "auc": self.participant.vars['task_rounds']['AUC'],

            "tou_verguetung": self.player.in_round(self.participant.vars['task_rounds']['TOU']).verguetung,
            "rtp_verguetung": self.player.in_round(self.participant.vars['task_rounds']['RTP']).verguetung,
            "pet_verguetung": self.player.in_round(self.participant.vars['task_rounds']['PET']).verguetung,
            "auc_verguetung": self.player.in_round(self.participant.vars['task_rounds']['AUC']).verguetung,

            "tou_satis": self.player.in_round(self.participant.vars['task_rounds']['TOU']).Zufrieden,
            "rtp_satis": self.player.in_round(self.participant.vars['task_rounds']['RTP']).Zufrieden,
            "pet_satis": self.player.in_round(self.participant.vars['task_rounds']['PET']).Zufrieden,
            "auc_satis": self.player.in_round(self.participant.vars['task_rounds']['AUC']).Zufrieden,

            "tou_complex": (self.player.in_round(self.participant.vars['task_rounds']['TOU']).Komplex + self.player.in_round(self.participant.vars['task_rounds']['TOU']).Anspruchsvoll + self.player.in_round(self.participant.vars['task_rounds']['TOU']).Denkvermoegen + self.player.in_round(self.participant.vars['task_rounds']['TOU']).Herausfordernd)/4,
            "rtp_complex": (self.player.in_round(self.participant.vars['task_rounds']['RTP']).Komplex + self.player.in_round(self.participant.vars['task_rounds']['RTP']).Anspruchsvoll + self.player.in_round(self.participant.vars['task_rounds']['RTP']).Denkvermoegen + self.player.in_round(self.participant.vars['task_rounds']['RTP']).Herausfordernd)/4,
            "pet_complex": (self.player.in_round(self.participant.vars['task_rounds']['PET']).Komplex + self.player.in_round(self.participant.vars['task_rounds']['PET']).Anspruchsvoll + self.player.in_round(self.participant.vars['task_rounds']['PET']).Denkvermoegen + self.player.in_round(self.participant.vars['task_rounds']['PET']).Herausfordernd)/4,
            "auc_complex": (self.player.in_round(self.participant.vars['task_rounds']['AUC']).Komplex + self.player.in_round(self.participant.vars['task_rounds']['AUC']).Anspruchsvoll + self.player.in_round(self.participant.vars['task_rounds']['AUC']).Denkvermoegen + self.player.in_round(self.participant.vars['task_rounds']['AUC']).Herausfordernd)/4,
        }

    def before_next_page(self):
        self.player.Spiel_Counter = self.round_number
        if self.player.Choice == 'TOU':
            self.player.R1_P1_player_vardemand = Constants.player_vardemand_tou[0][0]
            self.player.R1_P2_player_vardemand = Constants.player_vardemand_tou[0][1]
            self.player.R2_P1_player_vardemand = Constants.player_vardemand_tou[1][0]
            self.player.R2_P2_player_vardemand = Constants.player_vardemand_tou[1][1]

        elif self.player.Choice == 'RTP':
            self.player.R1_P1_player_vardemand = Constants.player_vardemand_rtp[0][0]
            self.player.R1_P2_player_vardemand = Constants.player_vardemand_rtp[0][1]
            self.player.R2_P1_player_vardemand = Constants.player_vardemand_rtp[1][0]
            self.player.R2_P2_player_vardemand = Constants.player_vardemand_rtp[1][1]

        elif self.player.Choice == 'PET':
            self.player.R1_P1_player_vardemand = Constants.player_vardemand_pet[0][0]
            self.player.R1_P2_player_vardemand = Constants.player_vardemand_pet[0][1]
            self.player.R2_P1_player_vardemand = Constants.player_vardemand_pet[1][0]
            self.player.R2_P2_player_vardemand = Constants.player_vardemand_pet[1][1]

        elif self.player.Choice == 'AUC':
            self.player.R1_P1_player_vardemand = Constants.player_vardemand_auc[0][0]
            self.player.R1_P2_player_vardemand = Constants.player_vardemand_auc[0][1]
            self.player.R2_P1_player_vardemand = Constants.player_vardemand_auc[1][0]
            self.player.R2_P2_player_vardemand = Constants.player_vardemand_auc[1][1]

class Metadaten2(Page):
    form_model = 'player'
    form_fields = ["Geschlecht", "Alter", "Hoechste_berufliche_Qualifikation", "Erwerbsstatus", "Einkommen", "FinalFeedback"]
    def is_displayed(self):
        return self.round_number == 5

class Metadaten(Page):
    form_model = 'player'
    form_fields = ["Risikobereitschaft"]
    def is_displayed(self):
        return self.round_number == 5


class Metadaten3(Page):
    form_model = 'player'
    form_fields = ["Choice2", "Feedback"]
    def is_displayed(self):
        return self.round_number == 5

    def before_next_page(self):
        self.session.vars['num_participants_finished'] = self.session.vars['num_participants_finished'] + 1


class TOU_Einfuehrung(Page):
    def is_displayed(self):
        return self.round_number == self.participant.vars['task_rounds']['TOU']

    def vars_for_template(self):

        self.player.game_played = "TOU"

        self.player.START_time_epoch = time.time()

        self.player.R1_P1_player_vardemand = Constants.player_vardemand_tou[0][0]
        self.player.R1_P2_player_vardemand = Constants.player_vardemand_tou[0][1]
        self.player.R2_P1_player_vardemand = Constants.player_vardemand_tou[1][0]
        self.player.R2_P2_player_vardemand = Constants.player_vardemand_tou[1][1]

        self.player.example_P1_vardemand = Constants.example_player_vardemand[0]
        self.player.example_P2_vardemand = Constants.example_player_vardemand[1]

        self.player.Spiel_Counter = self.round_number

        return {
            "Spiel_Counter": self.player.Spiel_Counter,
            "R1_P1_player_vardemand": Constants.player_vardemand_tou[0][0],
            "R1_P2_player_vardemand": Constants.player_vardemand_tou[0][1],

            "R1_P1_set_price": Constants.prices_tou[0][0],
            "R1_P2_set_price": Constants.prices_tou[0][1],
        }

    pass

class TOU_example(Page):
    form_model = 'player'
    form_fields = ["example_P1_vardemand", "example_P2_vardemand"]

    def is_displayed(self):
        return (self.round_number == self.participant.vars['task_rounds']['TOU'])
    def vars_for_template(self):

        return {
            "R1_Psum_player_vardemand": sum(Constants.example_player_vardemand),
            "Spiel_Counter": self.player.Spiel_Counter,

            "R1_P1_player_vardemand": Constants.example_player_vardemand[0],
            "R1_P2_player_vardemand": Constants.example_player_vardemand[1],

            "R1_P1_set_price": Constants.example_prices_tou[0],
            "R1_P2_set_price": Constants.example_prices_tou[1],
        }


    def error_message(self, values):

        if values['example_P1_vardemand'] + values['example_P2_vardemand'] != sum(Constants.example_player_vardemand):
            return 'You have to consume exactly ' + str(sum(Constants.example_player_vardemand)) +' energy units in this round.'
        if (values['example_P1_vardemand'] % 1) + (values['example_P2_vardemand'] % 1) != 0:
            return 'You can only enter whole numbers.'

    pass

class TOU_R1(Page):
    form_model = 'player'
    form_fields = ["R1_P1_player_vardemand", "R1_P2_player_vardemand"]

    def is_displayed(self):
        return (self.round_number == self.participant.vars['task_rounds']['TOU']) or (self.round_number == 5 and self.player.Choice == 'TOU')
    def vars_for_template(self):

        return {
            "R1_Psum_player_vardemand": sum(Constants.player_vardemand_tou[0]),
            "Spiel_Counter": self.player.Spiel_Counter,

            "R1_P1_player_vardemand": Constants.player_vardemand_tou[0][0],
            "R1_P2_player_vardemand": Constants.player_vardemand_tou[0][1],

            "R1_P1_set_price": Constants.prices_tou[0][0],
            "R1_P2_set_price": Constants.prices_tou[0][1],
        }


    def error_message(self, values):

        if values['R1_P1_player_vardemand'] + values['R1_P2_player_vardemand'] != (Constants.player_vardemand_tou[0][0] + Constants.player_vardemand_tou[0][1]):
            return 'You have to consume exactly ' + str(Constants.player_vardemand_tou[0][0] + Constants.player_vardemand_tou[0][1]) +' energy units in this round.'
        if (values['R1_P1_player_vardemand'] % 1) + (values['R1_P2_player_vardemand'] % 1) != 0:
            return 'You can only enter whole numbers.'

    pass

class TOU_R2(Page):
    form_model = 'player'
    form_fields = ["R2_P1_player_vardemand", "R2_P2_player_vardemand"]
    def is_displayed(self):
        return (self.round_number == self.participant.vars['task_rounds']['TOU']) or (self.round_number == 5 and self.player.Choice == 'TOU')
    def vars_for_template(self):

        return {
            "R2_Psum_player_vardemand": sum(Constants.player_vardemand_tou[1]),
            "Spiel_Counter": self.player.Spiel_Counter,

            "R2_P1_player_vardemand": Constants.player_vardemand_tou[1][0],
            "R2_P2_player_vardemand": Constants.player_vardemand_tou[1][1],

            "R2_P1_set_price": Constants.prices_tou[1][0],
            "R2_P2_set_price": Constants.prices_tou[1][1],
        }

    def error_message(self, values):

        if values['R2_P1_player_vardemand'] + values['R2_P2_player_vardemand'] != (Constants.player_vardemand_tou[1][0] + Constants.player_vardemand_tou[1][1]):
            return 'You have to consume exactly ' + str(Constants.player_vardemand_tou[1][0] + Constants.player_vardemand_tou[1][1]) +' energy units in this round.'
        if (values['R2_P1_player_vardemand'] % 1) + (values['R2_P2_player_vardemand'] % 1) != 0:
            return 'You can only enter whole numbers.'

    pass

class TOU_example_Result(Page):
    def is_displayed(self):
        return (self.round_number == self.participant.vars['task_rounds']['TOU'])
    def vars_for_template(self):
        R1_adjustment_cost = (abs(Constants.example_player_vardemand[0] - self.player.example_P1_vardemand) + abs(Constants.example_player_vardemand[1] - self.player.example_P2_vardemand)) / 2
        R1_adjustment_cost = round(R1_adjustment_cost, 1)
        R1_total_cost = ((self.player.example_P1_vardemand) * Constants.example_prices_tou[0]) + ((self.player.example_P2_vardemand) * Constants.example_prices_tou[1])

        # ces always fills up
        R1_P1_total_demand = self.player.example_P1_vardemand + Constants.example_competition_vardemand [0]
        R1_P2_total_demand = self.player.example_P2_vardemand + Constants.example_competition_vardemand [1]

        R1_P1_supply_ces = R1_P1_total_demand - Constants.example_res[0]
        R1_P2_supply_ces = R1_P2_total_demand - Constants.example_res[1]

        TOU_R1_total_cost = R1_total_cost + R1_adjustment_cost
        R1_average_price = round(R1_total_cost/sum(Constants.example_player_vardemand), 1)

        self.player.adjustment_cost_example = R1_adjustment_cost
        self.player.total_cost_example = TOU_R1_total_cost

        return {
            "TOU_R1_total_cost": TOU_R1_total_cost,
            "Spiel_Counter": self.player.Spiel_Counter,
            "costs_energy": R1_total_cost,

            "R1_P1_player_vardemand": self.player.example_P1_vardemand,
            "R1_P2_player_vardemand": self.player.example_P2_vardemand,

            "R1_player_total_demand":  sum(Constants.example_player_vardemand),

            "R1_P1_competition_vardemand": Constants.example_competition_vardemand[0],
            "R1_P2_competition_vardemand": Constants.example_competition_vardemand[1],

            "R1_P1_set_price": Constants.example_prices_tou[0],
            "R1_P2_set_price": Constants.example_prices_tou[1],

            "R1_P1_supply_res": Constants.example_res[0],
            "R1_P2_supply_res": Constants.example_res[1],

            "R1_P1_supply_ces": R1_P1_supply_ces,
            "R1_P2_supply_ces": R1_P2_supply_ces,

            "R1_adjustment_cost": R1_adjustment_cost,
            "R1_total_cost": R1_total_cost,
        }

    pass

class TOU_R1_Result(Page):
    def is_displayed(self):
        return (self.round_number == self.participant.vars['task_rounds']['TOU']) or (self.round_number == 5 and self.player.Choice == 'TOU')
    def vars_for_template(self):
        R1_adjustment_cost = (abs(Constants.player_vardemand_tou[0][0] - self.player.R1_P1_player_vardemand) + abs(Constants.player_vardemand_tou[0][1] - self.player.R1_P2_player_vardemand)) / 2
        R1_adjustment_cost = round(R1_adjustment_cost, 1)
        R1_total_cost = ((self.player.R1_P1_player_vardemand) * Constants.prices_tou[0][0]) + ((self.player.R1_P2_player_vardemand) * Constants.prices_tou[0][1])

        # ces always fills up
        R1_P1_total_demand = self.player.R1_P1_player_vardemand + Constants.competition_vardemand_tou[0][0]
        R1_P2_total_demand = self.player.R1_P2_player_vardemand + Constants.competition_vardemand_tou[0][1]

        R1_P1_supply_ces = R1_P1_total_demand - Constants.res_tou[0][0]
        R1_P2_supply_ces = R1_P2_total_demand - Constants.res_tou[0][1]

        TOU_R1_total_cost = R1_total_cost + R1_adjustment_cost
        R1_average_price = round(R1_total_cost/sum(Constants.player_vardemand_tou[0]), 1)

        self.player.total_adjustment_cost = self.player.total_adjustment_cost + R1_adjustment_cost
        self.player.total_cost_with_adjustment_cost = self.player.total_cost_with_adjustment_cost + TOU_R1_total_cost

        return {
            "TOU_R1_total_cost": TOU_R1_total_cost,
            "Spiel_Counter": self.player.Spiel_Counter,
            "costs_energy": R1_total_cost,

            "R1_P1_player_vardemand": self.player.R1_P1_player_vardemand,
            "R1_P2_player_vardemand": self.player.R1_P2_player_vardemand,

            "R1_player_total_demand":  sum(Constants.player_vardemand_tou[0]),

            "R1_P1_competition_vardemand": Constants.competition_vardemand_tou[0][0],
            "R1_P2_competition_vardemand": Constants.competition_vardemand_tou[0][1],

            "R1_P1_set_price": Constants.prices_tou[0][0],
            "R1_P2_set_price": Constants.prices_tou[0][1],

            "R1_P1_supply_res": Constants.res_tou[0][0],
            "R1_P2_supply_res": Constants.res_tou[0][1],

            "R1_P1_supply_ces": R1_P1_supply_ces,
            "R1_P2_supply_ces": R1_P2_supply_ces,

            "R1_adjustment_cost": R1_adjustment_cost,
            "R1_total_cost": R1_total_cost,
        }

    pass

class TOU_R2_Result(Page):
    def is_displayed(self):
        return (self.round_number == self.participant.vars['task_rounds']['TOU']) or (self.round_number == 5 and self.player.Choice == 'TOU')
    def vars_for_template(self):
        R2_adjustment_cost = (abs(Constants.player_vardemand_tou[1][0] - self.player.R2_P1_player_vardemand) + abs(Constants.player_vardemand_tou[1][1] - self.player.R2_P2_player_vardemand)) / 2
        R2_adjustment_cost = round(R2_adjustment_cost, 1)
        R2_total_cost = ((self.player.R2_P1_player_vardemand) * Constants.prices_tou[1][0]) + ((self.player.R2_P2_player_vardemand) * Constants.prices_tou[1][1])

        R2_player_total_demand = self.player.R2_P1_player_vardemand + self.player.R2_P2_player_vardemand
        R2_average_price = round((R2_total_cost / R2_player_total_demand), 1)

        # ces fills up
        R2_P1_total_demand = self.player.R2_P1_player_vardemand + Constants.competition_vardemand_tou[1][0]
        R2_P2_total_demand = self.player.R2_P2_player_vardemand + Constants.competition_vardemand_tou[1][1]

        R2_P1_supply_ces = R2_P1_total_demand - Constants.res_tou[1][0]
        R2_P2_supply_ces = R2_P2_total_demand - Constants.res_tou[1][1]

        TOU_R2_total_cost = R2_total_cost + R2_adjustment_cost

        self.player.total_adjustment_cost = self.player.total_adjustment_cost + R2_adjustment_cost
        self.player.total_cost_with_adjustment_cost = self.player.total_cost_with_adjustment_cost + TOU_R2_total_cost

        return {
            "TOU_R2_total_cost": TOU_R2_total_cost,
            "Spiel_Counter": self.player.Spiel_Counter,
            "costs_energy": R2_total_cost,

            "R2_P1_player_vardemand": self.player.R2_P1_player_vardemand,
            "R2_P2_player_vardemand": self.player.R2_P2_player_vardemand,

            "R2_player_total_demand": sum(Constants.player_vardemand_tou[1]),

            "R2_P1_competition_vardemand": Constants.competition_vardemand_tou[1][0],
            "R2_P2_competition_vardemand": Constants.competition_vardemand_tou[1][1],

            "R2_P1_set_price": Constants.prices_tou[1][0],
            "R2_P2_set_price": Constants.prices_tou[1][1],

            "R2_P1_supply_res": Constants.res_tou[1][0],
            "R2_P2_supply_res": Constants.res_tou[1][1],

            "R2_P1_supply_ces": R2_P1_supply_ces,
            "R2_P2_supply_ces": R2_P2_supply_ces,

            "R2_adjustment_cost": R2_adjustment_cost,
            "R2_total_cost": R2_total_cost,
        }

    pass


class TOU_Meinung(Page):
    form_model = 'player'
    form_fields = ["Komplex", "Anspruchsvoll", "Denkvermoegen", "Herausfordernd", "TOU_Attention"]
    def is_displayed(self):
        return (self.round_number == self.participant.vars['task_rounds']['TOU'])
    def vars_for_template(self):

        return {
            "Spiel_Counter": self.player.Spiel_Counter,

        }

class TOU_Result(Page):
    def is_displayed(self):
        return (self.round_number == self.participant.vars['task_rounds']['TOU']) or (self.round_number == 5 and self.player.Choice == 'TOU')
    def vars_for_template(self):

        self.player.verguetung = 100 - self.player.total_cost_with_adjustment_cost
        totalDemand = sum(sum(Constants.player_vardemand_tou,[]))

        self.player.ENDE_time_epoch = time.time()

        return {
            "Spiel_Counter": self.player.Spiel_Counter,
            "TOU_total_cost_with_adjustment_cost": self.player.total_cost_with_adjustment_cost,
            "TOU_verguetung": self.player.verguetung,
            "total_demand": totalDemand
        }

    pass

class TOU_Zufrieden(Page):
    form_model = 'player'
    form_fields = ["Zufrieden", "Feedback"]
    def is_displayed(self):
        return (self.round_number == self.participant.vars['task_rounds']['TOU'])

    def vars_for_template(self):

        return {
            "Spiel_Counter": self.player.Spiel_Counter,

        }

class RTP_Einfuehrung(Page):
    def is_displayed(self):
        return self.round_number == self.participant.vars['task_rounds']['RTP']

    def vars_for_template(self):
        self.player.START_time_epoch = time.time()

        self.player.game_played = "RTP"

        self.player.R1_P1_player_vardemand = Constants.player_vardemand_rtp[0][0]
        self.player.R1_P2_player_vardemand = Constants.player_vardemand_rtp[0][1]
        self.player.R2_P1_player_vardemand = Constants.player_vardemand_rtp[1][0]
        self.player.R2_P2_player_vardemand = Constants.player_vardemand_rtp[1][1]

        self.player.example_P1_vardemand = Constants.example_player_vardemand[0]
        self.player.example_P2_vardemand = Constants.example_player_vardemand[1]

        self.player.Spiel_Counter = self.round_number

        return {
            "Spiel_Counter": self.player.Spiel_Counter,
            "R1_P1_player_vardemand": Constants.player_vardemand_rtp[0][0],
            "R1_P2_player_vardemand": Constants.player_vardemand_rtp[0][1],
        }

    pass

class RTP_example_P1(Page):
    form_model = 'player'
    form_fields = ["example_P1_vardemand"]
    def is_displayed(self):
        return (self.round_number == self.participant.vars['task_rounds']['RTP'])
    def vars_for_template(self):
        R1_P1_rt_price = Constants.calculateRTP(self, Constants.example_res[0]/(Constants.example_player_vardemand[0] + Constants.example_competition_vardemand[0]))

        return {
            "Spiel_Counter": self.player.Spiel_Counter,

            "R1_P1_rt_price": R1_P1_rt_price,
            "R1_Psum_player_vardemand": sum(Constants.example_player_vardemand),

            "R1_P1_player_vardemand": self.player.example_P1_vardemand,
            "R1_P2_player_vardemand": self.player.example_P2_vardemand,
        }

    def error_message(self, values):

        if values['example_P1_vardemand'] > (sum(Constants.example_player_vardemand)):
            return 'The entire demand in this round is only ' + str(sum(Constants.example_player_vardemand))
        if (values['example_P1_vardemand'] % 1) != 0:
            return 'You can only enter whole numbers.'

    def before_next_page(self):

        self.player.example_P2_vardemand =  sum(Constants.example_player_vardemand) - self.player.example_P1_vardemand

class RTP_R1_P1(Page):
    form_model = 'player'
    form_fields = ["R1_P1_player_vardemand"]
    def is_displayed(self):
        return (self.round_number == self.participant.vars['task_rounds']['RTP']) or (self.round_number == 5 and self.player.Choice == 'RTP')
    def vars_for_template(self):
        R1_P1_rt_price = Constants.calculateRTP(self, Constants.res_rtp[0][0]/(Constants.player_vardemand_rtp[0][0]+Constants.competition_vardemand_rtp[0][0]))

        return {
            "Spiel_Counter": self.player.Spiel_Counter,

            "R1_P1_rt_price": R1_P1_rt_price,
            "R1_Psum_player_vardemand": sum(Constants.player_vardemand_rtp[0]),

            "R1_P1_player_vardemand": self.player.R1_P1_player_vardemand,
            "R1_P2_player_vardemand": self.player.R1_P2_player_vardemand,
        }

    def error_message(self, values):

        if values['R1_P1_player_vardemand'] > (sum(Constants.player_vardemand_rtp[0])):
            return 'The entire demand in this round is only ' + str(sum(Constants.player_vardemand_rtp[0]))
        if (values['R1_P1_player_vardemand'] % 1) != 0:
            return 'You can only enter whole numbers.'

    def before_next_page(self):

        self.player.R1_P2_player_vardemand =  sum(Constants.player_vardemand_rtp[0]) - self.player.R1_P1_player_vardemand


class RTP_R2_P1(Page):
    form_model = 'player'
    form_fields = ["R2_P1_player_vardemand"]
    def is_displayed(self):
        return (self.round_number == self.participant.vars['task_rounds']['RTP']) or (self.round_number == 5 and self.player.Choice == 'RTP')

    def vars_for_template(self):
        R2_P1_rt_price = Constants.calculateRTP(self, Constants.res_rtp[1][0]/(Constants.player_vardemand_rtp[1][0]+Constants.competition_vardemand_rtp[1][0]))

        return {
            "Spiel_Counter": self.player.Spiel_Counter,

            "R2_P1_rt_price": R2_P1_rt_price,

            "R2_P1_player_vardemand": self.player.R2_P1_player_vardemand,
            "R2_P2_player_vardemand": self.player.R2_P2_player_vardemand,

            "R2_Psum_player_vardemand": sum(Constants.player_vardemand_rtp[1]),

        }
    def error_message(self, values):

        if values['R2_P1_player_vardemand'] > (sum(Constants.player_vardemand_rtp[1])):
            return 'The entire demand in this round is only ' + str(sum(Constants.player_vardemand_rtp[1]))
        if (values['R2_P1_player_vardemand'] % 1) != 0:
            return 'You can only enter whole numbers.'

    def before_next_page(self):
        self.player.R2_P2_player_vardemand =  sum(Constants.player_vardemand_rtp[1]) - self.player.R2_P1_player_vardemand


class RTP_example_Result(Page):

    def is_displayed(self):
        return (self.round_number == self.participant.vars['task_rounds']['RTP'])

    def vars_for_template(self):
        R1_P1_rt_price = Constants.calculateRTP(self, Constants.example_res[0]/(Constants.example_player_vardemand[0] + Constants.example_competition_vardemand[0]))
        R1_P2_rt_price = Constants.calculateRTP(self, Constants.example_res[1]/(self.player.example_P2_vardemand + Constants.example_competition_vardemand[1]))

        R1_adjustment_cost = (abs(Constants.example_player_vardemand[0] - self.player.example_P1_vardemand) + abs(Constants.example_player_vardemand[1] - self.player.example_P2_vardemand)) / 2
        R1_adjustment_cost = round(R1_adjustment_cost, 1)

        R1_total_cost = ((self.player.example_P1_vardemand) * R1_P1_rt_price) + ((self.player.example_P2_vardemand) * R1_P2_rt_price)
        R1_player_total_demand = self.player.example_P1_vardemand + self.player.example_P2_vardemand
        R1_average_price = round((R1_total_cost / R1_player_total_demand), 1)

        R1_P1_total_demand = self.player.example_P1_vardemand + Constants.example_competition_vardemand[0]
        R1_P2_total_demand = self.player.example_P2_vardemand + Constants.example_competition_vardemand[1]

        R1_P1_supply_ces = R1_P1_total_demand - Constants.example_res[0]
        R1_P2_supply_ces = R1_P2_total_demand - Constants.example_res[1]

        RTP_R1_total_cost = R1_total_cost + R1_adjustment_cost

        self.player.adjustment_cost_example = R1_adjustment_cost
        self.player.total_cost_example = RTP_R1_total_cost

        return {
            "RTP_R1_total_cost": RTP_R1_total_cost,
            "Spiel_Counter": self.player.Spiel_Counter,
            "R1_average_price": R1_average_price,
            "costs_energy": R1_total_cost,

            "R1_P1_player_vardemand": self.player.example_P1_vardemand,
            "R1_P2_player_vardemand": self.player.example_P2_vardemand,

            "R1_player_total_demand": R1_player_total_demand,

            "R1_adjustment_cost": R1_adjustment_cost,

            "R1_P1_rt_price": R1_P1_rt_price,
            "R1_P2_rt_price": R1_P2_rt_price,

            "R1_P1_competition_vardemand": Constants.example_competition_vardemand[0],
            "R1_P2_competition_vardemand": Constants.example_competition_vardemand[1],

            "R1_P1_supply_res": Constants.example_res[0],
            "R1_P2_supply_res": Constants.example_res[1],

            "R1_P1_supply_ces": R1_P1_supply_ces,
            "R1_P2_supply_ces": R1_P2_supply_ces,
        }

    pass

class RTP_R1_Result(Page):

    def is_displayed(self):
        return (self.round_number == self.participant.vars['task_rounds']['RTP']) or (self.round_number == 5 and self.player.Choice == 'RTP')

    def vars_for_template(self):
        R1_P1_rt_price = Constants.calculateRTP(self, Constants.res_rtp[0][0]/(Constants.player_vardemand_rtp[0][0] + Constants.competition_vardemand_rtp[0][0]))
        R1_P2_rt_price = Constants.calculateRTP(self, Constants.res_rtp[0][1]/(self.player.R1_P2_player_vardemand + Constants.competition_vardemand_rtp[0][1]))

        R1_adjustment_cost = (abs(Constants.player_vardemand_rtp[0][0] - self.player.R1_P1_player_vardemand) + abs(Constants.player_vardemand_rtp[0][1] - self.player.R1_P2_player_vardemand)) / 2
        R1_adjustment_cost = round(R1_adjustment_cost, 1)

        R1_total_cost = ((self.player.R1_P1_player_vardemand) * R1_P1_rt_price) + ((self.player.R1_P2_player_vardemand) * R1_P2_rt_price)
        R1_player_total_demand = self.player.R1_P1_player_vardemand + self.player.R1_P2_player_vardemand
        R1_average_price = round((R1_total_cost / R1_player_total_demand), 1)

        R1_P1_total_demand = self.player.R1_P1_player_vardemand + Constants.competition_vardemand_rtp[0][0]
        R1_P2_total_demand = self.player.R1_P2_player_vardemand + Constants.competition_vardemand_rtp[0][1]

        R1_P1_supply_ces = R1_P1_total_demand - Constants.res_rtp[0][0]
        R1_P2_supply_ces = R1_P2_total_demand - Constants.res_rtp[0][1]

        RTP_R1_total_cost = R1_total_cost + R1_adjustment_cost

        self.player.total_adjustment_cost = self.player.total_adjustment_cost + R1_adjustment_cost
        self.player.total_cost_with_adjustment_cost = self.player.total_cost_with_adjustment_cost + RTP_R1_total_cost

        return {
            "RTP_R1_total_cost": RTP_R1_total_cost,
            "Spiel_Counter": self.player.Spiel_Counter,
            "R1_average_price": R1_average_price,
            "costs_energy": R1_total_cost,

            "R1_P1_player_vardemand": self.player.R1_P1_player_vardemand,
            "R1_P2_player_vardemand": self.player.R1_P2_player_vardemand,

            "R1_player_total_demand": R1_player_total_demand,

            "R1_adjustment_cost": R1_adjustment_cost,

            "R1_P1_rt_price": R1_P1_rt_price,
            "R1_P2_rt_price": R1_P2_rt_price,

            "R1_P1_competition_vardemand": Constants.competition_vardemand_rtp[0][0],
            "R1_P2_competition_vardemand": Constants.competition_vardemand_rtp[0][1],

            "R1_P1_supply_res": Constants.res_rtp[0][0],
            "R1_P2_supply_res": Constants.res_rtp[0][1],

            "R1_P1_supply_ces": R1_P1_supply_ces,
            "R1_P2_supply_ces": R1_P2_supply_ces,
        }

    pass

class RTP_R2_Result(Page):

    def is_displayed(self):
        return (self.round_number == self.participant.vars['task_rounds']['RTP']) or (self.round_number == 5 and self.player.Choice == 'RTP')
    def vars_for_template(self):
        R2_P1_rt_price = Constants.calculateRTP(self, Constants.res_rtp[1][0]/(Constants.player_vardemand_rtp[1][0] + Constants.competition_vardemand_rtp[1][0]))
        R2_P2_rt_price = Constants.calculateRTP(self, Constants.res_rtp[1][1]/(self.player.R2_P2_player_vardemand + Constants.competition_vardemand_rtp[1][1]))

        R2_adjustment_cost = (abs(Constants.player_vardemand_rtp[1][0] - self.player.R2_P1_player_vardemand) + abs(Constants.player_vardemand_rtp[1][1] - self.player.R2_P2_player_vardemand)) / 2
        R2_adjustment_cost = round(R2_adjustment_cost, 1)

        R2_total_cost = ((self.player.R2_P1_player_vardemand) * R2_P1_rt_price) + ((self.player.R2_P2_player_vardemand) * R2_P2_rt_price)
        R2_player_total_demand = self.player.R2_P1_player_vardemand + self.player.R2_P2_player_vardemand
        R2_average_price = round((R2_total_cost / R2_player_total_demand), 1)

        R2_P1_total_demand = self.player.R2_P1_player_vardemand + Constants.competition_vardemand_rtp[1][0]
        R2_P2_total_demand = self.player.R2_P2_player_vardemand + Constants.competition_vardemand_rtp[1][1]

        R2_P1_supply_ces = R2_P1_total_demand - Constants.res_rtp[1][0]
        R2_P2_supply_ces = R2_P2_total_demand - Constants.res_rtp[1][1]

        RTP_R2_total_cost = R2_total_cost + R2_adjustment_cost

        self.player.total_adjustment_cost = self.player.total_adjustment_cost + R2_adjustment_cost
        self.player.total_cost_with_adjustment_cost = self.player.total_cost_with_adjustment_cost + RTP_R2_total_cost

        return {
            "RTP_R2_total_cost": RTP_R2_total_cost,
            "Spiel_Counter": self.player.Spiel_Counter,
            "R2_average_price": R2_average_price,
            "costs_energy": R2_total_cost,

            "R2_P1_player_vardemand": self.player.R2_P1_player_vardemand,
            "R2_P2_player_vardemand": self.player.R2_P2_player_vardemand,

            "R2_player_total_demand": R2_player_total_demand,

            "R2_adjustment_cost": R2_adjustment_cost,

            "R2_P1_rt_price": R2_P1_rt_price,
            "R2_P2_rt_price": R2_P2_rt_price,

            "R2_P1_competition_vardemand": Constants.competition_vardemand_rtp[1][0],
            "R2_P2_competition_vardemand": Constants.competition_vardemand_rtp[1][1],

            "R2_P1_supply_res": Constants.res_rtp[1][0],
            "R2_P2_supply_res": Constants.res_rtp[1][1],

            "R2_P1_supply_ces": R2_P1_supply_ces,
            "R2_P2_supply_ces": R2_P2_supply_ces,
        }


class RTP_Meinung(Page):
    form_model = 'player'
    form_fields = ["Komplex", "Anspruchsvoll", "Denkvermoegen", "Herausfordernd",]
    def is_displayed(self):
        return (self.round_number == self.participant.vars['task_rounds']['RTP'])
    def vars_for_template(self):

        return {
            "Spiel_Counter": self.player.Spiel_Counter,

        }

class RTP_Result(Page):
    def is_displayed(self):
        return (self.round_number == self.participant.vars['task_rounds']['RTP']) or (self.round_number == 5 and self.player.Choice == 'RTP')

    def vars_for_template(self):
        self.player.verguetung = 100 - self.player.total_cost_with_adjustment_cost
        self.player.ENDE_time_epoch = time.time()
        totalDemand = sum(sum(Constants.player_vardemand_rtp,[]))

        return {
            "Spiel_Counter": self.player.Spiel_Counter,
            "RTP_total_cost_with_adjustment_cost": self.player.total_cost_with_adjustment_cost,
            "RTP_verguetung": self.player.verguetung,
            "total_demand": totalDemand
        }

class RTP_Zufrieden(Page):
    form_model = 'player'
    form_fields = ["Zufrieden", "Feedback"]
    def is_displayed(self):
        return (self.round_number == self.participant.vars['task_rounds']['RTP'])

    def vars_for_template(self):

        return {
            "Spiel_Counter": self.player.Spiel_Counter,

        }

class PET_Einfuehrung(Page):
    def is_displayed(self):
        return self.round_number == self.participant.vars['task_rounds']['PET']

    def vars_for_template(self):
        self.player.START_time_epoch = time.time()

        self.player.game_played = "PET"

        self.player.R1_P1_player_vardemand = Constants.player_vardemand_pet[0][0]
        self.player.R1_P2_player_vardemand = Constants.player_vardemand_pet[0][1]
        self.player.R2_P1_player_vardemand = Constants.player_vardemand_pet[1][0]
        self.player.R2_P2_player_vardemand = Constants.player_vardemand_pet[1][1]

        self.player.example_P1_vardemand = Constants.example_player_vardemand[0]
        self.player.example_P2_vardemand = Constants.example_player_vardemand[1]

        self.player.Spiel_Counter = self.round_number

        return {
            "Spiel_Counter": self.player.Spiel_Counter,

            "R1_P1_player_vardemand": self.player.R1_P1_player_vardemand,
            "R1_P2_player_vardemand": self.player.R1_P2_player_vardemand,
        }

    pass


class PET_R1_Bid(Page):
    form_model = 'player'
    form_fields = ["Rx_player_bid_pet"]
    def is_displayed(self):
        return (self.round_number == self.participant.vars['task_rounds']['PET']) or (self.round_number == 5 and self.player.Choice == 'PET')
    def vars_for_template(self):
        return {
            "Spiel_Counter": self.player.Spiel_Counter,
        }

    def error_message(self, values):

        if values['Rx_player_bid_pet'] != 1.0 and values['Rx_player_bid_pet'] != 1.5 and values[
            'Rx_player_bid_pet'] != 2.0 and values['Rx_player_bid_pet'] != 2.5 and values['Rx_player_bid_pet'] != 3.0 and \
                values['Rx_player_bid_pet'] != 3.5 and values['Rx_player_bid_pet'] != 4.0 and values[
            'Rx_player_bid_pet'] != 4.5 and values['Rx_player_bid_pet'] != 5.0 and values['Rx_player_bid_pet'] != 5.5:
            return 'You can only bid in steps of 0.5 from 1.0 to 5.0.'

    pass

class PET_example_Bid(Page):
    form_model = 'player'
    form_fields = ["example_player_bid_pet"]
    def is_displayed(self):
        return (self.round_number == self.participant.vars['task_rounds']['PET'])
    def vars_for_template(self):
        return {
            "Spiel_Counter": self.player.Spiel_Counter,
        }

    def error_message(self, values):

        if values['example_player_bid_pet'] != 1.0 and values['example_player_bid_pet'] != 1.5 and values[
            'example_player_bid_pet'] != 2.0 and values['example_player_bid_pet'] != 2.5 and values['example_player_bid_pet'] != 3.0 and \
                values['example_player_bid_pet'] != 3.5 and values['example_player_bid_pet'] != 4.0 and values[
            'example_player_bid_pet'] != 4.5 and values['example_player_bid_pet'] != 5.0 and values['example_player_bid_pet'] != 5.5:
            return 'You can only bid in steps of 0.5 from 1.0 to 5.0.'

    pass

class PET_example_Shift(Page):
    form_model = 'player'
    form_fields = ["example_P1_vardemand", "example_P2_vardemand"]
    def is_displayed(self):
        return (self.round_number == self.participant.vars['task_rounds']['PET'])
    def vars_for_template(self):
        if self.player.example_player_bid_pet >= Constants.example_competition_bid_pet:
            R1_player_rank = 1
        else:
            R1_player_rank = 2

        return {
            "R1_Psum_player_vardemand": sum(Constants.example_player_vardemand),
            "Spiel_Counter": self.player.Spiel_Counter,
            "competition_bid": Constants.example_competition_bid_pet,

            "R1_P1_player_vardemand": self.player.example_P1_vardemand,
            "R1_P2_player_vardemand": self.player.example_P2_vardemand,

            "R1_P1_player_bid": self.player.example_player_bid_pet,
            "R1_P1_player_rank": R1_player_rank,
        }

    def error_message(self, values):

        if values['example_P1_vardemand'] + values['example_P2_vardemand'] != sum(Constants.example_player_vardemand):
            return 'You have to consume exactly ' + str(sum(Constants.example_player_vardemand)) +' energy units in this round.'
        if (values['example_P1_vardemand'] % 1) + (values['example_P2_vardemand'] % 1) != 0:
            return 'You can only enter whole numbers.'


class PET_R1_Shift(Page):
    form_model = 'player'
    form_fields = ["R1_P1_player_vardemand", "R1_P2_player_vardemand"]
    def is_displayed(self):
        return (self.round_number == self.participant.vars['task_rounds']['PET']) or (self.round_number == 5 and self.player.Choice == 'PET')
    def vars_for_template(self):
        if self.player.Rx_player_bid_pet >= Constants.competition_bid_pet:
            R1_player_rank = 1
        else:
            R1_player_rank = 2

        return {
            "R1_Psum_player_vardemand": sum(Constants.player_vardemand_pet[0]),
            "Spiel_Counter": self.player.Spiel_Counter,
            "competition_bid": Constants.competition_bid_pet,

            "R1_P1_player_vardemand": self.player.R1_P1_player_vardemand,
            "R1_P2_player_vardemand": self.player.R1_P2_player_vardemand,

            "R1_P1_player_bid": self.player.Rx_player_bid_pet,
            "R1_P1_player_rank": R1_player_rank,
        }

    def error_message(self, values):
        if values['R1_P1_player_vardemand'] + values['R1_P2_player_vardemand'] != sum(Constants.player_vardemand_pet[0]):
            return 'You have to consume exactly ' + str(sum(Constants.player_vardemand_pet[0])) +' energy units in this round.'
        if (values['R1_P1_player_vardemand'] % 1) + (values['R1_P2_player_vardemand'] % 1) != 0:
            return 'You can only enter whole numbers.'


class PET_R2_Shift(Page):
    form_model = 'player'
    form_fields = ["R2_P1_player_vardemand", "R2_P2_player_vardemand"]
    def is_displayed(self):
        return (self.round_number == self.participant.vars['task_rounds']['PET']) or (self.round_number == 5 and self.player.Choice == 'PET')
    def vars_for_template(self):

        if self.player.Rx_player_bid_pet >= Constants.competition_bid_pet:
            R2_player_rank = 1
        else:
            R2_player_rank = 2

        return {
            "R2_Psum_player_vardemand": sum(Constants.player_vardemand_pet[1]),
            "Spiel_Counter": self.player.Spiel_Counter,

            "R2_P1_player_vardemand": self.player.R2_P1_player_vardemand,
            "R2_P2_player_vardemand": self.player.R2_P2_player_vardemand,
            "competition_bid": Constants.competition_bid_pet,

            "R2_P1_player_bid": self.player.Rx_player_bid_pet,
            "R2_P1_player_rank": R2_player_rank,
        }

    def error_message(self, values):

        if values['R2_P1_player_vardemand'] + values['R2_P2_player_vardemand'] != (
                sum(Constants.player_vardemand_pet[1])):
            return 'You have to consume exactly ' + str(
                sum(Constants.player_vardemand_pet[1])) + ' energy units in this round.'
        if (values['R2_P1_player_vardemand'] % 1) + (values['R2_P2_player_vardemand'] % 1) != 0:
            return 'You can only enter whole numbers.'


class PET_example_Result(Page):

    def is_displayed(self):
        return (self.round_number == self.participant.vars['task_rounds']['PET'])

    def vars_for_template(self):
        R1_adjustment_cost = (abs(Constants.example_player_vardemand[0] - self.player.example_P1_vardemand) + abs(Constants.example_player_vardemand[1] - self.player.example_P2_vardemand)) / 2
        R1_adjustment_cost = round(R1_adjustment_cost, 1)

        R1_P1_consumedAt5 = Constants.determineOverdemand(self, self.player.example_player_bid_pet>=Constants.example_competition_bid_pet, self.player.example_P1_vardemand, Constants.example_competition_vardemand[0], Constants.example_res[0])
        R1_P2_consumedAt5 = Constants.determineOverdemand(self, self.player.example_player_bid_pet >=Constants.example_competition_bid_pet, self.player.example_P2_vardemand,Constants.example_competition_vardemand[1],Constants.example_res[1])

        R1_total_cost = (self.player.example_P1_vardemand - R1_P1_consumedAt5) * self.player.example_player_bid_pet + R1_P1_consumedAt5*5.0 + (self.player.example_P2_vardemand - R1_P2_consumedAt5) * self.player.example_player_bid_pet + R1_P2_consumedAt5*5.0
        R1_total_cost = round(R1_total_cost, 2)

        R1_P1_total_demand = self.player.example_P1_vardemand + Constants.example_competition_vardemand[0]
        R1_P2_total_demand = self.player.example_P2_vardemand + Constants.example_competition_vardemand[1]

        R1_P1_supply_ces = R1_P1_total_demand - Constants.example_res[0]
        R1_P2_supply_ces = R1_P2_total_demand - Constants.example_res[1]

        PET_R1_total_cost = R1_total_cost + R1_adjustment_cost

        self.player.adjustment_cost_example = R1_adjustment_cost
        self.player.total_cost_example = PET_R1_total_cost

        return {
            "R1_player_bid_energy": self.player.example_P1_vardemand + self.player.example_P2_vardemand - R1_P1_consumedAt5 - R1_P2_consumedAt5,
            "R1_P1_player_bid": self.player.example_player_bid_pet,
            "R1_player_5_energy": R1_P1_consumedAt5 + R1_P2_consumedAt5,
            "R1_adjustment_cost": R1_adjustment_cost,
            "PET_R1_total_cost": PET_R1_total_cost,

            "R1_player_5_morning": R1_P1_consumedAt5,
            "R1_player_5_afternoon": R1_P2_consumedAt5,
            "total_demand": Constants.example_player_vardemand[0] + Constants.example_player_vardemand[1],

            "R1_P1_competition_vardemand": Constants.example_competition_vardemand[0],
            "R1_P2_competition_vardemand": Constants.example_competition_vardemand[1],

            "R1_P1_player_vardemand": self.player.example_P1_vardemand,
            "R1_P2_player_vardemand": self.player.example_P2_vardemand,

            "R1_P1_supply_ces": R1_P1_supply_ces,
            "R1_P2_supply_ces": R1_P2_supply_ces,

            "R1_P1_save_res": Constants.example_res[0],
            "R1_P2_save_res": Constants.example_res[1],

            "Spiel_Counter": self.player.Spiel_Counter,
        }

class PET_R1_Result(Page):

    def is_displayed(self):
        return (self.round_number == self.participant.vars['task_rounds']['PET']) or (self.round_number == 5 and self.player.Choice == 'PET')

    def vars_for_template(self):
        R1_adjustment_cost = (abs(Constants.player_vardemand_pet[0][0] - self.player.R1_P1_player_vardemand) + abs(Constants.player_vardemand_pet[0][1] - self.player.R1_P2_player_vardemand)) / 2
        R1_adjustment_cost = round(R1_adjustment_cost, 1)

        R1_P1_consumedAt5 = Constants.determineOverdemand(self, self.player.Rx_player_bid_pet>=Constants.competition_bid_pet, self.player.R1_P1_player_vardemand, Constants.competition_vardemand_pet[0][0], Constants.res_pet[0][0])
        R1_P2_consumedAt5 = Constants.determineOverdemand(self, self.player.Rx_player_bid_pet >=Constants.competition_bid_pet, self.player.R1_P2_player_vardemand,Constants.competition_vardemand_pet[0][1],Constants.res_pet[0][1])

        R1_total_cost = (self.player.R1_P1_player_vardemand - R1_P1_consumedAt5) * self.player.Rx_player_bid_pet + R1_P1_consumedAt5*5.0 + (self.player.R1_P2_player_vardemand - R1_P2_consumedAt5) * self.player.Rx_player_bid_pet + R1_P2_consumedAt5*5.0
        R1_total_cost = round(R1_total_cost, 2)

        R1_P1_total_demand = self.player.R1_P1_player_vardemand + Constants.competition_vardemand_pet[0][0]
        R1_P2_total_demand = self.player.R1_P2_player_vardemand + Constants.competition_vardemand_pet[0][1]

        R1_P1_supply_ces = R1_P1_total_demand - Constants.res_pet[0][0]
        R1_P2_supply_ces = R1_P2_total_demand - Constants.res_pet[0][1]

        PET_R1_total_cost = R1_total_cost + R1_adjustment_cost

        self.player.total_adjustment_cost = self.player.total_adjustment_cost + R1_adjustment_cost
        self.player.total_cost_with_adjustment_cost = self.player.total_cost_with_adjustment_cost + PET_R1_total_cost

        return {
            "R1_player_bid_energy": self.player.R1_P1_player_vardemand + self.player.R1_P2_player_vardemand - R1_P1_consumedAt5 - R1_P2_consumedAt5,
            "R1_P1_player_bid": self.player.Rx_player_bid_pet,
            "R1_player_5_energy": R1_P1_consumedAt5 + R1_P2_consumedAt5,
            "R1_adjustment_cost": R1_adjustment_cost,
            "PET_R1_total_cost": PET_R1_total_cost,

            "R1_P1_competition_vardemand": Constants.competition_vardemand_pet[0][0],
            "R1_P2_competition_vardemand": Constants.competition_vardemand_pet[0][1],

            "R1_player_5_morning": R1_P1_consumedAt5,
            "R1_player_5_afternoon": R1_P2_consumedAt5,
            "total_demand": Constants.player_vardemand_pet[0][0] + Constants.player_vardemand_pet[0][1],

            "R1_P1_player_vardemand": self.player.R1_P1_player_vardemand,
            "R1_P2_player_vardemand": self.player.R1_P2_player_vardemand,

            "R1_P1_supply_ces": R1_P1_supply_ces,
            "R1_P2_supply_ces": R1_P2_supply_ces,

            "R1_P1_save_res": Constants.res_pet[0][0],
            "R1_P2_save_res": Constants.res_pet[0][1],

            "Spiel_Counter": self.player.Spiel_Counter,
        }

class PET_R2_Result(Page):

    def is_displayed(self):
        return (self.round_number == self.participant.vars['task_rounds']['PET']) or (self.round_number == 5 and self.player.Choice == 'PET')

    def vars_for_template(self):
        R2_adjustment_cost = (abs(Constants.player_vardemand_pet[1][0] - self.player.R2_P1_player_vardemand) + abs(Constants.player_vardemand_pet[1][1] - self.player.R2_P2_player_vardemand)) / 2
        R2_adjustment_cost = round(R2_adjustment_cost, 1)

        R2_P1_consumedAt5 = Constants.determineOverdemand(self, self.player.Rx_player_bid_pet >=Constants.competition_bid_pet,self.player.R2_P1_player_vardemand,Constants.competition_vardemand_pet[1][0],Constants.res_pet[1][0])
        R2_P2_consumedAt5 = Constants.determineOverdemand(self, self.player.Rx_player_bid_pet >=Constants.competition_bid_pet,self.player.R2_P2_player_vardemand,Constants.competition_vardemand_pet[1][1],Constants.res_pet[1][1])

        R2_total_cost = (self.player.R2_P1_player_vardemand - R2_P1_consumedAt5) * self.player.Rx_player_bid_pet + R2_P1_consumedAt5 * 5.0 + (self.player.R2_P2_player_vardemand - R2_P2_consumedAt5) * self.player.Rx_player_bid_pet + R2_P2_consumedAt5 * 5.0
        R2_total_cost = round(R2_total_cost, 2)

        R2_P1_total_demand = self.player.R2_P1_player_vardemand + Constants.competition_vardemand_pet[1][0]
        R2_P2_total_demand = self.player.R2_P2_player_vardemand + Constants.competition_vardemand_pet[1][1]

        R2_P1_supply_ces = R2_P1_total_demand - Constants.res_pet[1][0]
        R2_P2_supply_ces = R2_P2_total_demand - Constants.res_pet[1][1]

        PET_R2_total_cost = R2_total_cost + R2_adjustment_cost

        self.player.total_adjustment_cost = self.player.total_adjustment_cost + R2_adjustment_cost
        self.player.total_cost_with_adjustment_cost = self.player.total_cost_with_adjustment_cost + PET_R2_total_cost

        return {
            "R2_player_bid_energy": self.player.R2_P1_player_vardemand + self.player.R2_P2_player_vardemand - R2_P1_consumedAt5 - R2_P2_consumedAt5,
            "R2_P1_player_bid": self.player.Rx_player_bid_pet,
            "R2_player_5_energy": R2_P1_consumedAt5 + R2_P2_consumedAt5,
            "R2_adjustment_cost": R2_adjustment_cost,
            "PET_R2_total_cost": PET_R2_total_cost,

            "R2_player_5_morning": R2_P1_consumedAt5,
            "R2_player_5_afternoon": R2_P2_consumedAt5,
            "total_demand": Constants.player_vardemand_pet[1][0] + Constants.player_vardemand_pet[1][1],

            "R2_P1_competition_vardemand": Constants.competition_vardemand_pet[1][0],
            "R2_P2_competition_vardemand": Constants.competition_vardemand_pet[1][1],

            "R2_P1_player_vardemand": self.player.R2_P1_player_vardemand,
            "R2_P2_player_vardemand": self.player.R2_P2_player_vardemand,

            "R2_P1_supply_ces": R2_P1_supply_ces,
            "R2_P2_supply_ces": R2_P2_supply_ces,

            "R2_P1_save_res": Constants.res_pet[1][0],
            "R2_P2_save_res": Constants.res_pet[1][1],

            "Spiel_Counter": self.player.Spiel_Counter,
        }



class PET_Meinung(Page):
    form_model = 'player'
    form_fields = ["Komplex", "Anspruchsvoll", "Denkvermoegen", "Herausfordernd",]
    def is_displayed(self):
        return (self.round_number == self.participant.vars['task_rounds']['PET'])
    def vars_for_template(self):

        return {
            "Spiel_Counter": self.player.Spiel_Counter,
        }

class PET_Result(Page):
    def is_displayed(self):
        return (self.round_number == self.participant.vars['task_rounds']['PET']) or (self.round_number == 5 and self.player.Choice == 'PET')

    def vars_for_template(self):
        self.player.ENDE_time_epoch = time.time()
        self.player.verguetung = 100 - self.player.total_cost_with_adjustment_cost
        totalDemand = sum(sum(Constants.player_vardemand_pet,[]))

        return {
            "Spiel_Counter": self.player.Spiel_Counter,
            "PET_total_cost_with_adjustment_cost": self.player.total_cost_with_adjustment_cost,
            "total_demand": totalDemand,
            "PET_verguetung": self.player.verguetung,
        }

    pass

class PET_Zufrieden(Page):
    form_model = 'player'
    form_fields = ["Zufrieden", "Feedback", "PET_Attention"]
    def is_displayed(self):
        return (self.round_number == self.participant.vars['task_rounds']['PET'])

    def vars_for_template(self):

        return {
            "Spiel_Counter": self.player.Spiel_Counter,

        }

class AUC_Einfuehrung(Page):
    def is_displayed(self):
        return self.round_number == self.participant.vars['task_rounds']['AUC']
    def vars_for_template(self):
        self.player.START_time_epoch = time.time()

        self.player.game_played = "AUC"

        self.player.R1_P1_player_vardemand = Constants.player_vardemand_auc[0][0]
        self.player.R1_P2_player_vardemand = Constants.player_vardemand_auc[0][1]
        self.player.R2_P1_player_vardemand = Constants.player_vardemand_auc[1][0]
        self.player.R2_P2_player_vardemand = Constants.player_vardemand_auc[1][1]

        self.player.example_P1_vardemand = Constants.example_player_vardemand[0]
        self.player.example_P2_vardemand = Constants.example_player_vardemand[1]

        self.player.Spiel_Counter = self.round_number

        return {
            "Spiel_Counter": self.player.Spiel_Counter,

            "R1_P1_player_vardemand": self.player.R1_P1_player_vardemand,
            "R1_P2_player_vardemand": self.player.R1_P2_player_vardemand,
        }

    pass

class AUC_example_P1_Bid(Page):
    form_model = 'player'
    form_fields = ["example_P1_player_bid_auc"]
    def is_displayed(self):
        return (self.round_number == self.participant.vars['task_rounds']['AUC'])
    def vars_for_template(self):
        return {
            "Spiel_Counter": self.player.Spiel_Counter,
            "demand": self.player.example_P1_vardemand,
        }

    def error_message(self, values):
        if values['example_P1_player_bid_auc'] != 1.0 and values['example_P1_player_bid_auc'] != 1.5 and values[
            'example_P1_player_bid_auc'] != 2.0 and values['example_P1_player_bid_auc'] != 2.5 and values['example_P1_player_bid_auc'] != 3.0 and \
                values['example_P1_player_bid_auc'] != 3.5 and values['example_P1_player_bid_auc'] != 4.0 and values[
            'example_P1_player_bid_auc'] != 4.5 and values['example_P1_player_bid_auc'] != 5.0 and values['example_P1_player_bid_auc'] != 5.5:
            return 'You can only bid in steps of 0.5 from 1.0 to 5.0.'

class AUC_example_P2_Bid(Page):
    form_model = 'player'
    form_fields = ["example_P2_player_bid_auc"]
    def is_displayed(self):
        return (self.round_number == self.participant.vars['task_rounds']['AUC'])
    def vars_for_template(self):
        return {
            "Spiel_Counter": self.player.Spiel_Counter,
            "demand": self.player.example_P2_vardemand,
        }
    def error_message(self, values):
        if values['example_P2_player_bid_auc'] != 1.0 and values['example_P2_player_bid_auc'] != 1.5 and values[
            'example_P2_player_bid_auc'] != 2.0 and values['example_P2_player_bid_auc'] != 2.5 and values['example_P2_player_bid_auc'] != 3.0 and \
                values['example_P2_player_bid_auc'] != 3.5 and values['example_P2_player_bid_auc'] != 4.0 and values[
            'example_P2_player_bid_auc'] != 4.5 and values['example_P2_player_bid_auc'] != 5.0 and values['example_P2_player_bid_auc'] != 5.5:
            return 'You can only bid in steps of 0.5 from 1.0 to 5.0.'

class AUC_R1_P1_Bid(Page):
    form_model = 'player'
    form_fields = ["R1_P1_player_bid_auc"]
    def is_displayed(self):
        return (self.round_number == self.participant.vars['task_rounds']['AUC']) or (self.round_number == 5 and self.player.Choice == 'AUC')
    def vars_for_template(self):
        return {
            "Spiel_Counter": self.player.Spiel_Counter,
            "demand": self.player.R1_P1_player_vardemand,
        }

    def error_message(self, values):
        if values['R1_P1_player_bid_auc'] != 1.0 and values['R1_P1_player_bid_auc'] != 1.5 and values[
            'R1_P1_player_bid_auc'] != 2.0 and values['R1_P1_player_bid_auc'] != 2.5 and values['R1_P1_player_bid_auc'] != 3.0 and \
                values['R1_P1_player_bid_auc'] != 3.5 and values['R1_P1_player_bid_auc'] != 4.0 and values[
            'R1_P1_player_bid_auc'] != 4.5 and values['R1_P1_player_bid_auc'] != 5.0 and values['R1_P1_player_bid_auc'] != 5.5:
            return 'You can only bid in steps of 0.5 from 1.0 to 5.0.'

class AUC_R1_P2_Bid(Page):
    form_model = 'player'
    form_fields = ["R1_P2_player_bid_auc"]
    def is_displayed(self):
        return (self.round_number == self.participant.vars['task_rounds']['AUC']) or (self.round_number == 5 and self.player.Choice == 'AUC')
    def vars_for_template(self):
        return {
            "Spiel_Counter": self.player.Spiel_Counter,
            "demand": self.player.R1_P2_player_vardemand,
        }
    def error_message(self, values):
        if values['R1_P2_player_bid_auc'] != 1.0 and values['R1_P2_player_bid_auc'] != 1.5 and values[
            'R1_P2_player_bid_auc'] != 2.0 and values['R1_P2_player_bid_auc'] != 2.5 and values['R1_P2_player_bid_auc'] != 3.0 and \
                values['R1_P2_player_bid_auc'] != 3.5 and values['R1_P2_player_bid_auc'] != 4.0 and values[
            'R1_P2_player_bid_auc'] != 4.5 and values['R1_P2_player_bid_auc'] != 5.0 and values['R1_P2_player_bid_auc'] != 5.5:
            return 'You can only bid in steps of 0.5 from 1.0 to 5.0.'

class AUC_R2_P1_Bid(Page):
    form_model = 'player'
    form_fields = ["R2_P1_player_bid_auc"]
    def is_displayed(self):
        return (self.round_number == self.participant.vars['task_rounds']['AUC']) or (self.round_number == 5 and self.player.Choice == 'AUC')
    def vars_for_template(self):
        return {
            "Spiel_Counter": self.player.Spiel_Counter,
            "demand": self.player.R2_P1_player_vardemand,
        }
    def error_message(self, values):
        if values['R2_P1_player_bid_auc'] != 1.0 and values['R2_P1_player_bid_auc'] != 1.5 and values[
            'R2_P1_player_bid_auc'] != 2.0 and values['R2_P1_player_bid_auc'] != 2.5 and values['R2_P1_player_bid_auc'] != 3.0 and \
                values['R2_P1_player_bid_auc'] != 3.5 and values['R2_P1_player_bid_auc'] != 4.0 and values[
            'R2_P1_player_bid_auc'] != 4.5 and values['R2_P1_player_bid_auc'] != 5.0 and values['R2_P1_player_bid_auc'] != 5.5:
            return 'You can only bid in steps of 0.5 from 1.0 to 5.0.'

class AUC_R2_P2_Bid(Page):
    form_model = 'player'
    form_fields = ["R2_P2_player_bid_auc"]
    def is_displayed(self):
        return (self.round_number == self.participant.vars['task_rounds']['AUC']) or (self.round_number == 5 and self.player.Choice == 'AUC')
    def vars_for_template(self):
        return {
            "Spiel_Counter": self.player.Spiel_Counter,
            "demand": self.player.R2_P2_player_vardemand,
        }
    def error_message(self, values):
        if values['R2_P2_player_bid_auc'] != 1.0 and values['R2_P2_player_bid_auc'] != 1.5 and values[
            'R2_P2_player_bid_auc'] != 2.0 and values['R2_P2_player_bid_auc'] != 2.5 and values['R2_P2_player_bid_auc'] != 3.0 and \
                values['R2_P2_player_bid_auc'] != 3.5 and values['R2_P2_player_bid_auc'] != 4.0 and values[
            'R2_P2_player_bid_auc'] != 4.5 and values['R2_P2_player_bid_auc'] != 5.0 and values['R2_P2_player_bid_auc'] != 5.5:
            return 'You can only bid in steps of 0.5 from 1.0 to 5.0.'

class AUC_example_P1(Page):
    form_model = 'player'
    form_fields = ["example_P1_vardemand"]
    def is_displayed(self):
        return (self.round_number == self.participant.vars['task_rounds']['AUC'])
    def vars_for_template(self):

        if self.player.example_P1_player_bid_auc >= Constants.example_competition_bid_auc[0]:
            R1_P1_player_rank = 1
        else:
            R1_P1_player_rank = 2

        return {
            "Spiel_Counter": self.player.Spiel_Counter,
            "R1_P1_player_rank": R1_P1_player_rank,
            "R1_P1_player_bid": self.player.example_P1_player_bid_auc,
            "R1_Psum_player_vardemand": sum(Constants.example_player_vardemand),
            "competition_bid": Constants.example_competition_bid_auc[0],

            "R1_P1_player_vardemand": self.player.example_P1_vardemand,
            "R1_P2_player_vardemand": self.player.example_P2_vardemand,
        }

    def error_message(self, values):
        if values['example_P1_vardemand'] > (sum(Constants.example_player_vardemand)):
            return 'The entire demand in this round is only ' + str(sum(Constants.example_player_vardemand))
        if (values['example_P1_vardemand'] % 1) != 0:
            return 'You can only enter whole numbers.'
    pass

    def before_next_page(self):
        self.player.example_P2_vardemand = sum(Constants.example_player_vardemand) - self.player.example_P1_vardemand

class AUC_R1_P1(Page):
    form_model = 'player'
    form_fields = ["R1_P1_player_vardemand"]
    def is_displayed(self):
        return (self.round_number == self.participant.vars['task_rounds']['AUC']) or (self.round_number == 5 and self.player.Choice == 'AUC')
    def vars_for_template(self):

        if self.player.R1_P1_player_bid_auc >= Constants.competition_bid_auc[0][0]:
            R1_P1_player_rank = 1
        else:
            R1_P1_player_rank = 2

        return {
            "Spiel_Counter": self.player.Spiel_Counter,
            "R1_P1_player_rank": R1_P1_player_rank,
            "R1_P1_player_bid": self.player.R1_P1_player_bid_auc,
            "R1_Psum_player_vardemand": sum(Constants.player_vardemand_auc[0]),
            "competition_bid": Constants.competition_bid_auc[0][0],

            "R1_P1_player_vardemand": self.player.R1_P1_player_vardemand,
            "R1_P2_player_vardemand": self.player.R1_P2_player_vardemand,
        }

    def error_message(self, values):
        if values['R1_P1_player_vardemand'] > (sum(Constants.player_vardemand_auc[0])):
            return 'The entire demand in this round is only ' + str(sum(Constants.player_vardemand_auc[0]))
        if (values['R1_P1_player_vardemand'] % 1) != 0:
            return 'You can only enter whole numbers.'
    pass

    def before_next_page(self):
        self.player.R1_P2_player_vardemand = sum(Constants.player_vardemand_auc[0]) - self.player.R1_P1_player_vardemand

class AUC_R2_P1(Page):
    form_model = 'player'
    form_fields = ["R2_P1_player_vardemand"]
    def is_displayed(self):
        return (self.round_number == self.participant.vars['task_rounds']['AUC']) or (self.round_number == 5 and self.player.Choice == 'AUC')
    def vars_for_template(self):

        if self.player.R2_P1_player_bid_auc >= Constants.competition_bid_auc[1][0]:
            R2_P1_player_rank = 1
        else:
            R2_P1_player_rank = 2

        return {
            "Spiel_Counter": self.player.Spiel_Counter,
            "R2_P1_player_rank": R2_P1_player_rank,
            "R2_P1_player_bid": self.player.R2_P1_player_bid_auc,
            "R2_Psum_player_vardemand": sum(Constants.player_vardemand_auc[1]),
            "competition_bid": Constants.competition_bid_auc[1][0],

            "R2_P1_player_vardemand": self.player.R2_P1_player_vardemand,
            "R2_P2_player_vardemand": self.player.R2_P2_player_vardemand,
        }

    def error_message(self, values):
        if values['R2_P1_player_vardemand'] > (sum(Constants.player_vardemand_auc[1])):
            return 'The entire demand in this round is only ' + str(
                sum(Constants.player_vardemand_auc[1]))
        if (values['R2_P1_player_vardemand'] % 1) != 0:
            return 'You can only enter whole numbers.'

    pass

    def before_next_page(self):
        self.player.R2_P2_player_vardemand = sum(
            Constants.player_vardemand_auc[1]) - self.player.R2_P1_player_vardemand

class AUC_example_Result(Page):
    def is_displayed(self):
        return (self.round_number == self.participant.vars['task_rounds']['AUC'])
    def vars_for_template(self):

        R1_adjustment_cost = (abs(Constants.example_player_vardemand[0] - self.player.example_P1_vardemand) + abs(Constants.example_player_vardemand[1] - self.player.example_P2_vardemand)) / 2
        R1_adjustment_cost = round(R1_adjustment_cost, 1)

        R1_P1_consumedAt5 = Constants.determineOverdemand(self, self.player.example_P1_player_bid_auc >=Constants.example_competition_bid_auc[0],self.player.example_P1_vardemand,Constants.example_competition_vardemand[0],Constants.example_res[0])
        R1_P2_consumedAt5 = Constants.determineOverdemand(self, self.player.example_P2_player_bid_auc >=Constants.example_competition_bid_auc[1],self.player.example_P2_vardemand,Constants.example_competition_vardemand[1],Constants.example_res[1])

        R1_total_cost = (self.player.example_P1_vardemand - R1_P1_consumedAt5) * self.player.example_P1_player_bid_auc + R1_P1_consumedAt5 * 5.0 + (self.player.example_P2_vardemand - R1_P2_consumedAt5) * self.player.example_P2_player_bid_auc + R1_P2_consumedAt5 * 5.0
        R1_total_cost = round(R1_total_cost, 2)

        R1_P1_total_demand = self.player.example_P1_vardemand + Constants.example_competition_vardemand[0]
        R1_P2_total_demand = self.player.example_P2_vardemand + Constants.example_competition_vardemand[1]

        R1_P1_supply_ces = R1_P1_total_demand - Constants.example_res[0]
        R1_P2_supply_ces = R1_P2_total_demand - Constants.example_res[1]

        AUC_R1_total_cost = R1_total_cost + R1_adjustment_cost

        self.player.adjustment_cost_example = R1_adjustment_cost
        self.player.total_cost_example = AUC_R1_total_cost

        if self.player.example_P2_player_bid_auc >= Constants.example_competition_bid_auc[1]:
            rank = 1
        else:
            rank = 2

        return {

            "AUC_R1_total_cost": AUC_R1_total_cost,
            "Spiel_Counter": self.player.Spiel_Counter,
            "R1_player_bid_energy": self.player.example_P1_vardemand + self.player.example_P2_vardemand - R1_P1_consumedAt5 - R1_P2_consumedAt5,
            "total_demand": self.player.example_P1_vardemand + self.player.example_P2_vardemand,
            "R1_player_5_morning": R1_P1_consumedAt5,
            "R1_player_5_afternoon": R1_P2_consumedAt5,

            "R1_player_5_energy": R1_P1_consumedAt5 + R1_P2_consumedAt5,
            "R1_adjustment_cost": R1_adjustment_cost,

            "R1_P1_competition_vardemand": Constants.example_competition_vardemand[0],
            "R1_P2_competition_vardemand": Constants.example_competition_vardemand[1],

            "R1_P1_player_vardemand": self.player.example_P1_vardemand,
            "R1_P2_player_vardemand": self.player.example_P2_vardemand,

            "R1_P1_supply_ces": R1_P1_supply_ces,
            "R1_P2_supply_ces": R1_P2_supply_ces,

            "R1_P1_save_res": Constants.example_res[0],
            "R1_P2_save_res": Constants.example_res[1],

            "R1_P1_player_bid": self.player.example_P1_player_bid_auc,
            "R1_P2_player_bid": self.player.example_P2_player_bid_auc,

            "rank": rank,
            "competition_bid": Constants.example_competition_bid_auc[1],

        }

class AUC_R1_Result(Page):
    def is_displayed(self):
        return (self.round_number == self.participant.vars['task_rounds']['AUC']) or (self.round_number == 5 and self.player.Choice == 'AUC')
    def vars_for_template(self):

        R1_adjustment_cost = (abs(Constants.player_vardemand_auc[0][0] - self.player.R1_P1_player_vardemand) + abs(Constants.player_vardemand_auc[0][1] - self.player.R1_P2_player_vardemand)) / 2
        R1_adjustment_cost = round(R1_adjustment_cost, 1)

        R1_P1_consumedAt5 = Constants.determineOverdemand(self, self.player.R1_P1_player_bid_auc >=Constants.competition_bid_auc[0][0],self.player.R1_P1_player_vardemand,Constants.competition_vardemand_auc[0][0],Constants.res_auc[0][0])
        R1_P2_consumedAt5 = Constants.determineOverdemand(self, self.player.R1_P2_player_bid_auc >=Constants.competition_bid_auc[0][1],self.player.R1_P2_player_vardemand,Constants.competition_vardemand_auc[0][1],Constants.res_auc[0][1])

        R1_total_cost = (self.player.R1_P1_player_vardemand - R1_P1_consumedAt5) * self.player.R1_P1_player_bid_auc + R1_P1_consumedAt5 * 5.0 + (self.player.R1_P2_player_vardemand - R1_P2_consumedAt5) * self.player.R1_P2_player_bid_auc + R1_P2_consumedAt5 * 5.0
        R1_total_cost = round(R1_total_cost, 2)

        R1_P1_total_demand = self.player.R1_P1_player_vardemand + Constants.competition_vardemand_auc[0][0]
        R1_P2_total_demand = self.player.R1_P2_player_vardemand + Constants.competition_vardemand_auc[0][1]

        R1_P1_supply_ces = R1_P1_total_demand - Constants.res_auc[0][0]
        R1_P2_supply_ces = R1_P2_total_demand - Constants.res_auc[0][1]

        AUC_R1_total_cost = R1_total_cost + R1_adjustment_cost
        R1_average_price = R1_total_cost/sum(Constants.player_vardemand_auc[0])

        self.player.total_adjustment_cost = self.player.total_adjustment_cost + R1_adjustment_cost
        self.player.total_cost_with_adjustment_cost = self.player.total_cost_with_adjustment_cost + AUC_R1_total_cost

        if self.player.R1_P2_player_bid_auc >= Constants.competition_bid_auc[0][1]:
            rank = 1
        else:
            rank = 2

        return {

            "AUC_R1_total_cost": AUC_R1_total_cost,
            "Spiel_Counter": self.player.Spiel_Counter,
            "R1_player_bid_energy": self.player.R1_P1_player_vardemand + self.player.R1_P2_player_vardemand - R1_P1_consumedAt5 - R1_P2_consumedAt5,
            "total_demand": self.player.R1_P1_player_vardemand + self.player.R1_P2_player_vardemand,
            "R1_player_5_morning": R1_P1_consumedAt5,
            "R1_player_5_afternoon": R1_P2_consumedAt5,

            "R1_average_price": R1_average_price,
            "R1_player_5_energy": R1_P1_consumedAt5 + R1_P2_consumedAt5,
            "R1_adjustment_cost": R1_adjustment_cost,

            "R1_P1_competition_vardemand": Constants.competition_vardemand_auc[0][0],
            "R1_P2_competition_vardemand": Constants.competition_vardemand_auc[0][1],

            "R1_P1_player_vardemand": self.player.R1_P1_player_vardemand,
            "R1_P2_player_vardemand": self.player.R1_P2_player_vardemand,

            "R1_P1_supply_ces": R1_P1_supply_ces,
            "R1_P2_supply_ces": R1_P2_supply_ces,

            "R1_P1_save_res": Constants.res_auc[0][0],
            "R1_P2_save_res": Constants.res_auc[0][1],

            "R1_P1_player_bid": self.player.R1_P1_player_bid_auc,
            "R1_P2_player_bid": self.player.R1_P2_player_bid_auc,

            "rank": rank,
            "competition_bid": Constants.competition_bid_auc[0][1],
        }

class AUC_R2_Result(Page):
    def is_displayed(self):
        return (self.round_number == self.participant.vars['task_rounds']['AUC']) or (self.round_number == 5 and self.player.Choice == 'AUC')
    def vars_for_template(self):

        R2_adjustment_cost = (abs(Constants.player_vardemand_auc[1][0] - self.player.R2_P1_player_vardemand) + abs(Constants.player_vardemand_auc[1][1] - self.player.R2_P2_player_vardemand)) / 2
        R2_adjustment_cost = round(R2_adjustment_cost, 1)

        R2_P1_consumedAt5 = Constants.determineOverdemand(self, self.player.R2_P1_player_bid_auc >=Constants.competition_bid_auc[1][0],self.player.R2_P1_player_vardemand,Constants.competition_vardemand_auc[1][0],Constants.res_auc[1][0])
        R2_P2_consumedAt5 = Constants.determineOverdemand(self, self.player.R2_P2_player_bid_auc >=Constants.competition_bid_auc[1][1],self.player.R2_P2_player_vardemand,Constants.competition_vardemand_auc[1][1],Constants.res_auc[1][1])

        R2_total_cost = (self.player.R2_P1_player_vardemand - R2_P1_consumedAt5) * self.player.R2_P1_player_bid_auc + R2_P1_consumedAt5 * 5.0 + (self.player.R2_P2_player_vardemand - R2_P2_consumedAt5) * self.player.R2_P2_player_bid_auc + R2_P2_consumedAt5 * 5.0
        R2_total_cost = round(R2_total_cost, 2)

        R2_P1_total_demand = self.player.R2_P1_player_vardemand + Constants.competition_vardemand_auc[1][0]
        R2_P2_total_demand = self.player.R2_P2_player_vardemand + Constants.competition_vardemand_auc[1][1]

        R2_P1_supply_ces = R2_P1_total_demand - Constants.res_auc[1][0]
        R2_P2_supply_ces = R2_P2_total_demand - Constants.res_auc[1][1]

        AUC_R2_total_cost = R2_total_cost + R2_adjustment_cost
        R2_average_price = R2_total_cost/sum(Constants.player_vardemand_auc[1])

        self.player.total_adjustment_cost = self.player.total_adjustment_cost + R2_adjustment_cost
        self.player.total_cost_with_adjustment_cost = self.player.total_cost_with_adjustment_cost + AUC_R2_total_cost

        if self.player.R2_P2_player_bid_auc >= Constants.competition_bid_auc[1][1]:
            rank = 1
        else:
            rank = 2

        return {

            "AUC_R2_total_cost": AUC_R2_total_cost,
            "Spiel_Counter": self.player.Spiel_Counter,
            "R2_player_bid_energy": self.player.R2_P1_player_vardemand + self.player.R2_P2_player_vardemand - R2_P1_consumedAt5 - R2_P2_consumedAt5,
            "total_demand": self.player.R2_P1_player_vardemand + self.player.R2_P2_player_vardemand,
            "R2_player_5_morning": R2_P1_consumedAt5,
            "R2_player_5_afternoon": R2_P2_consumedAt5,

            "R2_average_price": R2_average_price,
            "R2_player_5_energy": R2_P1_consumedAt5 + R2_P2_consumedAt5,
            "R2_adjustment_cost": R2_adjustment_cost,

            "R2_P1_player_vardemand": self.player.R2_P1_player_vardemand,
            "R2_P2_player_vardemand": self.player.R2_P2_player_vardemand,

            "R2_P1_competition_vardemand": Constants.competition_vardemand_auc[1][0],
            "R2_P2_competition_vardemand": Constants.competition_vardemand_auc[1][1],

            "R2_P1_supply_ces": R2_P1_supply_ces,
            "R2_P2_supply_ces": R2_P2_supply_ces,

            "R2_P1_save_res": Constants.res_auc[1][0],
            "R2_P2_save_res": Constants.res_auc[1][1],

            "R2_P1_player_bid": self.player.R2_P1_player_bid_auc,
            "R2_P2_player_bid": self.player.R2_P2_player_bid_auc,

            "rank": rank,
            "competition_bid": Constants.competition_bid_auc[1][1],
        }


class AUC_Meinung(Page):
    form_model = 'player'
    form_fields = ["Komplex", "Anspruchsvoll", "Denkvermoegen", "Herausfordernd",]
    def is_displayed(self):
        return (self.round_number == self.participant.vars['task_rounds']['AUC'])

    def vars_for_template(self):

        return {
            "Spiel_Counter": self.player.Spiel_Counter,

        }

class AUC_Result(Page):
    def is_displayed(self):
        return (self.round_number == self.participant.vars['task_rounds']['AUC']) or (self.round_number == 5 and self.player.Choice == 'AUC')
    def vars_for_template(self):
        self.player.ENDE_time_epoch = time.time()
        self.player.verguetung = 100 - self.player.total_cost_with_adjustment_cost
        totalDemand = sum(sum(Constants.player_vardemand_auc,[]))


        return {
            "Spiel_Counter": self.player.Spiel_Counter,
            "AUC_total_cost_with_adjustment_cost": self.player.total_cost_with_adjustment_cost,
            "total_demand": totalDemand,
            "AUC_verguetung": self.player.verguetung,
        }

    pass

class AUC_Zufrieden(Page):
    form_model = 'player'
    form_fields = ["Zufrieden", "Feedback"]
    def is_displayed(self):
        return (self.round_number == self.participant.vars['task_rounds']['AUC'])

    def vars_for_template(self):

        return {
            "Spiel_Counter": self.player.Spiel_Counter,

        }

class ENDE(Page):
    form_model = 'player'
    def is_displayed(self):
        return self.round_number == 5

    def vars_for_template(self):
        self.player.ERWIRTSCHAFTET = self.player.in_round(1).verguetung + self.player.in_round(2).verguetung + self.player.in_round(3).verguetung + self.player.in_round(4).verguetung + self.player.in_round(5).verguetung
        self.player.ERWIRTSCHAFTET = round(self.player.ERWIRTSCHAFTET, 1)

        self.player.game_played = self.player.Choice + "-5"

        self.player.player_id = self.participant.code
        return {
            "ERWIRTSCHAFTET": self.player.ERWIRTSCHAFTET,
            "ERWIRTSCHAFTET_EURO": self.player.ERWIRTSCHAFTET/100,

        }

class ENDE2(Page):

    def is_displayed(self):
        return self.round_number == 5

class AttentionCheckFailed(Page):

    def is_displayed(self):
        return (self.round_number == self.participant.vars['task_rounds']['TOU'] and self.player.field_maybe_none('TOU_Attention') != 4) or (self.round_number == self.participant.vars['task_rounds']['PET'] and self.player.field_maybe_none('PET_Attention') != 1)

class TestQuestionsFailed(Page):

    def is_displayed(self):
        return self.round_number == 1 and (self.player.field_maybe_none('Quiz1') != 4 or self.player.field_maybe_none('Quiz2') != 2)


page_sequence = [ErklaerungConsent, Erklaerung1, Erklaerung2, Quiz, Erklaerung1, Erklaerung2, Quiz, Wahl, TestQuestionsFailed,
                 TOU_Einfuehrung, TOU_example, TOU_example_Result, TOU_R1, TOU_R1_Result, TOU_R2, TOU_R2_Result, TOU_Meinung, TOU_Result, TOU_Zufrieden,
                 RTP_Einfuehrung, RTP_example_P1, RTP_example_Result, RTP_R1_P1, RTP_R1_Result, RTP_R2_P1, RTP_R2_Result, RTP_Meinung, RTP_Result, RTP_Zufrieden,
                 PET_Einfuehrung, PET_example_Bid, PET_example_Shift, PET_example_Result, PET_R1_Bid, PET_R1_Shift, PET_R1_Result, PET_R2_Shift, PET_R2_Result, PET_Meinung, PET_Result, PET_Zufrieden,
                 AUC_Einfuehrung, AUC_example_P1_Bid, AUC_example_P1, AUC_example_P2_Bid, AUC_example_Result, AUC_R1_P1_Bid, AUC_R1_P1, AUC_R1_P2_Bid, AUC_R1_Result, AUC_R2_P1_Bid, AUC_R2_P1, AUC_R2_P2_Bid, AUC_R2_Result, AUC_Meinung, AUC_Result, AUC_Zufrieden,
                 Metadaten2, Metadaten, Metadaten3, ENDE, ENDE2, AttentionCheckFailed]