from pliers.utils import progress_bar_wrapper
from pliers.stimuli import VideoStim
from pliers.converters import FrameSamplingConverter
from pliers import config
from .utils import get_test_data_path
from tqdm import tqdm
from os.path import join


def test_progress_bar(capsys):

    video_dir = join(get_test_data_path(), 'video')
    video = VideoStim(join(video_dir, 'obama_speech.mp4'))
    conv = FrameSamplingConverter(hertz=2)

    old_val = config.progress_bar
    config.progress_bar = True

    derived = conv.transform(video)
    out, err = capsys.readouterr()
    print("OUTPUT:", out, "\nERROR:", err)
    assert 'Video frame:' in out and '100%' in out

    config.progress_bar = False
    derived = conv.transform(video)
    out, err = capsys.readouterr()
    assert 'Video frame:' not in out and '100%' not in out

    config.progress_bar = old_val
