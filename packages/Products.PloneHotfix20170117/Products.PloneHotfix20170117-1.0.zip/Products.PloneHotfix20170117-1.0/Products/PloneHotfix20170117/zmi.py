from App.special_dtml import DTMLFile
from OFS.FindSupport import FindSupport

import pkg_resources

try:
    pkg_resources.get_distribution('Products.ExternalEditor')
except pkg_resources.DistributionNotFound:
    pass
else:
    import Products.ExternalEditor  # noqa force this patch to be done first

# Add external editor icon in breadcrumbs under tabs
FindSupport.manage_findResult = DTMLFile(
    'www/findResult', globals(), management_view='Find')
