from src.Gui.components import ExerciseComboBox, IntervalIcon, IntervalEntry, OnlineIntergration
import tkinter as tk
from tkinter import ttk
from src.DbManager import ConfigReader
from src.utils.constants import DatabaseConstants


class SettingNotebook(ttk.Notebook):
    setting_dict = {}

    def __init__(self, parent=None):
        super().__init__(master=parent)

        ## {} if file not found ##
        setting_dict = ConfigReader(DatabaseConstants.SETTINGS_YAML_PATH).read_config_file()
        

        self.tab = {}
        ## CREATE FRAME ##
        self.tab['Exercise'] = MuscleSetting(parent=self)
        self.tab['Save to'] = OnlineIntergration(parent=self,setting_dict=setting_dict)
        test_frame = tk.Frame(master=self)

        ## ADD FRAME TO NOTEBOOK ##
        for name, instance in self.tab.items():
            self.add(instance, text=name)
            self.add(instance, text=name)
        self.add(test_frame, text='save')

        tk.Button(test_frame, text='save here',command=self.save_all_data).pack()

    def save_all_data(self):
        all_dict_combined = {}
        for instance in self.tab.values():
            all_dict_combined.update(instance.get_info())

        ConfigReader().update_or_create_yaml_file(DatabaseConstants.SETTINGS_YAML_PATH,all_dict_combined)
        # ConfigReader().update_or_create_yaml_file(DatabaseConstants.SETTINGS_YAML_PATH,newdata)

class MuscleSetting(tk.Frame):
    def __init__(self, parent=None):
        super().__init__(master=parent)

        self.notify_var = tk.StringVar(value='')

        ## Timer settings ##
        timer_frame = tk.Frame(master=self)
        timer_frame.pack(fill='x')
        interval_icon = IntervalIcon(parent=timer_frame, img_path=r'C:\Scripts\01_PYTHON\Projects\Workout_Reminder\resources\icons\setting_gui\clock.png',
                                     text='Interval (min)')
        interval_icon.pack(side='left', fill='x', padx=10, pady=10)

        self.interval_entry = IntervalEntry(timer_frame)
        self.interval_entry.pack(side='left', fill='x', padx=10, pady=10)

        # MESSAGE
        self.notify_label = ttk.Label(
            master=self, textvariable=self.notify_var)
        self.notify_label.pack()

        ## COMBOBOX FRAME ##
        self.combo_frame = tk.Frame(master=self)
        self.combo_frame.pack(expand=True, fill='x')
        self.equipment_combi = ExerciseComboBox(
            parent=self.combo_frame, column_name='equipment', string_var=self.notify_var)
        self.equipment_combi.pack(fill='x', padx=5, pady=5)

        self.difficulty_combi = ExerciseComboBox(
            parent=self.combo_frame, column_name='difficulty', string_var=self.notify_var)
        self.difficulty_combi.pack(fill='x', padx=5, pady=5)

        self.muscle_combi = ExerciseComboBox(
            parent=self.combo_frame, column_name='muscle', string_var=self.notify_var)
        self.muscle_combi.pack(fill='x', padx=5, pady=5)

        self.cycle_muscle_var = tk.BooleanVar(value=False)
        self.cycle_muscle = ttk.Checkbutton(master=self.combo_frame, text='Target all Muscles', 
                                            command=self.save_all_muscles_setting,
                                            onvalue=True, offvalue=False, variable=self.cycle_muscle_var)
        self.cycle_muscle.pack( padx=5, pady=5)

        ## BUTTONS FRAME ##
        button_frame = tk.Frame(master=self)
        button_frame.pack(fill='x', padx=5, pady=2)

        # all_muscles_button = ttk.Button(
        #     master=button_frame, text='All Muscles', command=self.save_all_muscles_setting)
        # all_muscles_button.pack(side='left', fill='x',
        #                         expand=True, padx=5, pady=2)

        # save_button = ttk.Button(
        #     master=button_frame, text='Save', command=self.save_user_settings)
        # save_button.pack(side='left', fill='x', expand=True, padx=5, pady=2)

    def check_interval_entry(self):
        entry_text = self.interval_entry.get()
        if not entry_text:
            self.notify_var.set("Interval cannot be Empty")
            return False

        elif entry_text.isdigit():
            return True
        else:
            self.notify_var.set("Interval cannot be a string")
            return False

    def get_info(self):

        if self.cycle_muscle_var.get():
            muscle = 'default'
        else:
            muscle = self.muscle_combi.get()

        setting_data = {'equipment': self.equipment_combi.get(),
                        'muscle': muscle,
                        'difficulty': self.difficulty_combi.get()}

        for_data_base = {'database': setting_data,
                         'schedule': self.interval_entry.get()}

        # ConfigReader().update_or_create_yaml_file(
        #     DatabaseConstants.SETTINGS_YAML_PATH, for_data_base)
        return for_data_base

    def save_user_settings(self):

        if self.check_interval_entry():  # if interval entry is int then TRUE
            if self.equipment_combi.get() and self.difficulty_combi.get() and self.muscle_combi.get():
                self.get_info(cyle_muscle_group=True)
            else:
                self.notify_var.set('Select all the fields')

    def save_all_muscles_setting(self):
        equipment_entry_value = self.equipment_combi.get()
        # check if the user selected equipment or not
        if self.check_interval_entry():
            if self.equipment_combi.get() and self.difficulty_combi.get():
                pass
            else:
                self.notify_var.set('Select Equipment and Difficulty')


if __name__ == '__main__':
    # listboxes()
    # reference()
    root = tk.Tk()
    setting_gui = SettingNotebook(parent=root).pack()
    # setting_gui.lift(aboveThis=root)

    root.mainloop()
