from warehouse import Warehouse

if __name__ == "__main__":
    wh = Warehouse(10,10)
    wh.get_blocks_from_csv("blocks.csv")
    print(wh.is_spot_available(1,1,1,1))
    wh.place_block(0,1,1)
    print(wh.warehouse_matrix)
    print(wh.blocks_dict[1].x_origin, wh.blocks_dict[1].y_origin)
    print(wh.is_spot_available(1,1,5,5))
    wh.remove_block(0)
    print(wh.warehouse_matrix)
    print(wh.blocks_dict[1].x_origin, wh.blocks_dict[1].y_origin)

