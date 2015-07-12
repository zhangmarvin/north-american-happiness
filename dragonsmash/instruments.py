from client import Note

def noteFactoryFactory(instrument):
    def instrumentNoteFactory(frequency, duration, velocity, offset):
        return Note(frequency, instrument, duration, velocity, offset)
    return instrumentNoteFactory

Piano = noteFactoryFactory('Acoustic Grand')
Keyboard = noteFactoryFactory('Electric Piano 1')
Marimba = noteFactoryFactory('Marimba')
AcousticGuitar = noteFactoryFactory('Steel String Guitar')
ElectricGuitar = noteFactoryFactory('Electric Clean Guitar')
Bass = noteFactoryFactory('Electric Bass(finger)')
Violin = noteFactoryFactory('Violin')
Trumpet = noteFactoryFactory('Trumpet')
Saxophone = noteFactoryFactory('Alto Sax')

__all__ = [
    'Piano',
    'Keyboard',
    'Marimba',
    'AcousticGuitar',
    'ElectricGuitar',
    'Bass',
    'Violin',
    'Trumpet',
    'Saxophone',
]
