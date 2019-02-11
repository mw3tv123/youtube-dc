from tkinter import ttk


class PercentageLabel(ttk.Style):
    """A customized Style to display Percentage Label in a Progress Bar"""
    def __init__(self):
        """Constructor"""
        ttk.Style.__init__(self)
        # Add label in the layout
        self.layout('text.Horizontal.TProgressbar', [('Horizontal.Progressbar.trough',
                                                      {'children': [('Horizontal.Progressbar.pbar',
                                                                     {'side': 'left', 'sticky': 'ns'})],
                                                       'sticky': 'nswe'}),
                                                     ('Horizontal.Progressbar.label', {'sticky': ''})])
        # Set initial text
        self.configure('text.Horizontal.TProgressbar', text='0 %')
