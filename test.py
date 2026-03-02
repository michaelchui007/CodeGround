from decimal import Decimal

from templetes.rotate_layer.utils import CoordConverter

if __name__ == '__main__':
    a = "11111"
    a = CoordConverter.format_display(a)
    print(a)