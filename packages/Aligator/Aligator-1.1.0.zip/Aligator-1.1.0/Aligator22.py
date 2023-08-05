def List8(self,alt=-99):
    for each_item in self:
        if isinstance(each_item, list):
            List8(each_item,alt+1)
        else:
            for tab_stop in range(alt):
                print("\t",end='')
            print(each_item)
