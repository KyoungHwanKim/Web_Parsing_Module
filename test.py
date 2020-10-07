t = "http://218.146.55.65/g5/bbs/board.php?bo_table=notice&sop=and&sst=wr_datetime&sod=asc&page=1&device=pc"
if '?' in t:
    link = t[:t.index('?')]
    print(link)