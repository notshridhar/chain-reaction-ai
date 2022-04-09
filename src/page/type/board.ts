export type BoardCellState = {
    playerIndex: number,
    blobCount: number,
};

export type BoardState = Array<Array<BoardCellState>>;

export type BoardProps = {
    rowCount: number,
    colCount: number,
};
