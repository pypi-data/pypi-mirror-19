import pandas as pd
import warnings


class Dict(dict):

    def count(self, key, value=1):
        self.value_type = int
        if key in self:
            self[key] += value
        else:
            self[key] = value

    def append(self, key, value):
        self.value_type = list
        if key in self:
            self[key].append(value)
        else:
            self[key] = [value]

    def extend(self, key, values):
        self.value_type = list
        if key in self:
            self[key].extend(values)
        else:
            self[key] = values

    def add(self, key, value):
        self.value_type = set
        if key in self:
            self[key].add(value)
        else:
            self[key] = {value}

    def values_to_set(self):
        self.value_type = set
        for k, v in self.iteritems():
            self[k] = set(v)

    def len(self, key):
        return len(self[key]) if key in self else 0

    def to_csv(self, fp_out, columns=('k', 'v'), sort_values=True, sort_ascending=True, n_head=False):
        csv = pd.DataFrame(self.items(), columns=columns)
        if sort_values:
            csv.sort_values(columns[1], ascending=sort_ascending, inplace=True)
        if n_head:
            csv.head(n_head).to_csv(fp_out, index=False)
        else:
            csv.to_csv(fp_out, index=False)
