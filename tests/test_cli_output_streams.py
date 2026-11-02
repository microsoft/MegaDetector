"""Wrapper output streams only: fake model boundary, no downloads or inference."""
import importlib.util
import json
from pathlib import Path
import sys
import types
import pytest

@pytest.fixture
def cli(monkeypatch):
    source=Path(__file__).parents[1]/'src'/'megadetector_core'/'cli.py'
    spec=importlib.util.spec_from_file_location('cli_streams_under_test',source)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    calls=[]
    class Model:
        def __init__(self,**kwargs):calls.append(('init',kwargs))
        def single_image_detection(self,path):
            calls.append(('image',path))
            return {'detections':None}
    package=types.ModuleType('megadetector_core');package.MegaDetectorV6=Model
    monkeypatch.setitem(sys.modules,'megadetector_core',package)
    return module,calls

@pytest.mark.parametrize('directory',[False,True])
@pytest.mark.parametrize('output_file',[False,True])
def test_wrapper_keeps_json_and_progress_in_separate_streams(cli,tmp_path,capsys,directory,output_file):
    module,calls=cli
    images=tmp_path/'images';images.mkdir()
    image=images/'image.jpg';image.write_bytes(b'fake model does not read this')
    output=tmp_path/'results.json' if output_file else None
    args=types.SimpleNamespace(input=str(images if directory else image),output=str(output) if output else None,
                               device='cpu',model='MDV6-yolov9-c',threshold=.2)
    module.detect(args)
    captured=capsys.readouterr()
    data=json.loads(output.read_text() if output else captured.out)
    assert data==[{'file':str(image),'detections':[]}]
    if output_file:assert captured.out==''
    assert 'Loading MegaDetector' in captured.err
    assert 'Summary: 1 images, 0 detections, 0 images with animals' in captured.err
    assert ('Processed 1/1' if directory else 'Processing ') in captured.err
    assert calls==[('init',{'device':'cpu','pretrained':True,'version':'MDV6-yolov9-c'}),('image',str(image))]

@pytest.mark.parametrize('empty_directory',[False,True])
def test_input_errors_stay_on_stderr(cli,tmp_path,capsys,empty_directory):
    module,calls=cli
    source=tmp_path/'empty'
    if empty_directory:source.mkdir()
    args=types.SimpleNamespace(input=str(source),output=None,device='cpu',model='MDV6-yolov9-c',threshold=.2)
    with pytest.raises(SystemExit) as error:module.detect(args)
    assert error.value.code==1
    streams=capsys.readouterr()
    assert streams.out==''
    assert ('No image files found' if empty_directory else 'does not exist') in streams.err
    assert not any(c[0]=='image' for c in calls)
