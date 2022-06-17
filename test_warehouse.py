from warehouse import Warehouse

if __name__ == "__main__":
    wh = Warehouse(10,10)
    wh.get_blocks_from_csv("blocks.csv")
    wh.place_block(1,1,1)
    print(wh.warehouse_matrix)
    print(wh.blocks_dict[1].x_origin, wh.blocks_dict[1].y_origin)
    wh.remove_block(1)
    print(wh.warehouse_matrix)
    print(wh.blocks_dict[1].x_origin, wh.blocks_dict[1].y_origin)

