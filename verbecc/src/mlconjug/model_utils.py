from typing import Optional
from importlib_resources import as_file, files
import os
import pickle
from zipfile import ZipFile

from verbecc.src.utils.log_utils import LogUtils
from verbecc.src.defs.types.lang_code import LangCodeISO639_1
from verbecc.src.mlconjug.model import Model

_logger = LogUtils.get_logger(__name__)


def get_model_zip_filename(lang: LangCodeISO639_1) -> str:
    return "data/models/trained_model-{}.zip".format(lang)


def get_model_pickle_filename(lang: LangCodeISO639_1) -> str:
    return "trained_model-{0}.pickle".format(lang)


def save_model(model: Model) -> None:
    pickle_filename = get_model_pickle_filename(model.lang)
    with open(pickle_filename, "wb") as f:
        pickle.dump(model, f)
    zip_filename = get_model_zip_filename(model.lang)
    zip_path = files("verbecc") / zip_filename
    with as_file(zip_path) as f:
        with ZipFile(f, mode="w") as zf:
            zf.write(pickle_filename)
            _logger.info(
                "Saved model pickle filename %s to zip filename %s.",
                pickle_filename,
                zip_filename,
            )
    os.remove(pickle_filename)


def load_model(lang: LangCodeISO639_1) -> Optional[Model]:
    model = None
    zip_filename = get_model_zip_filename(lang)
    try:
        zip_path = files("verbecc") / zip_filename
        with as_file(zip_path) as f:
            with ZipFile(f) as zf:
                pickle_filename = get_model_pickle_filename(lang)
                with zf.open(pickle_filename, "r") as model_pickle:
                    model = pickle.loads(model_pickle.read())
                    _logger.info(
                        "Loaded model pickle filename %s from zip filename %s",
                        pickle_filename,
                        zip_filename,
                    )
    except Exception as ex:
        _logger.warning(
            "Exception loading model %s: %s", zip_filename, ex, exc_info=True
        )
    return model
