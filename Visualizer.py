class Visualizer:
    def __init__(self, model=None, name=None):
        if model is not None:
            self.model = model
        if name is not None:
            self.model_name = name

    def _flatten_model(self, modules, start_name):
        def flatten_list(_2d_list):
            flat_list = []
            # Iterate through the outer list
            for element in _2d_list:
                if type(element) is list:
                    # If the element is of type list, iterate through the sublist
                    for item in element:
                        flat_list.append(item)
                else:
                    flat_list.append(element)
            return flat_list

        ret = []
        names = []
        if str(modules._modules.items()) == "odict_items([])":  # so its an element and not a struct
            ret.append(modules)
            names = [start_name]
        else:
            for name, n in modules._modules.items():
                r, o = self._flatten_model(n, start_name)
                ret.append(r)
                names.append(
                    [x + "." + name + "." + str(r[o.index(x)].__class__).split(".")[-1].replace("'>", "") for x in o])

        return flatten_list(ret), flatten_list(names)

    def _get_learnable_parts(self, net, basename=None):
        if basename is None:
            basename = str(net.__class__).split(".")[-1].replace("'>", "")
        parts, names = self._flatten_model(net, basename)
        for p in parts:
            yield p, names[parts.index(p)]

    def flatten_model(self):
        return self._flatten_model(self.model, self.model_name)

    def get_learnable_parts(self, use_name=None):
        if use_name is None:
            return self._get_learnable_parts(self.model, self.model_name)
        else:
            return self._get_learnable_parts(self.model, use_name)
