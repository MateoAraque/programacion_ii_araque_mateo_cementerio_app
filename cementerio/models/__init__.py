# Re-exportamos: Django solo registra los modelos que llegan a importarse
from cementerio.models.sector import Sector
from cementerio.models.difunto import Difunto
from cementerio.models.tumba import Tumba
from cementerio.models.servicio import Servicio

__all__ = ['Sector', 'Difunto', 'Tumba', 'Servicio']
