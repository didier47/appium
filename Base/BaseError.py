from Base.BaseElementEnmu import Element


def get_error(kw):
    elements = {
        Element.TIME_OUT: lambda: "==%s request timeout==" % kw["element_info"],
        Element.NO_SUCH: lambda: "==%s no existe==" % kw["element_info"],
        Element.WEB_DROVER_EXCEPTION: lambda: "==%s error de controlador==" % kw["element_info"],
        Element.INDEX_ERROR: lambda: "==%s error de índice==" % kw["element_info"],
        Element.STALE_ELEMENT_REFERENCE_EXCEPTION: lambda: "==%s elemento de página ha ocurrido==" % kw["element_info"],
        Element.DEFAULT_ERROR: lambda: "==Por favor, marque %s==" % kw["element_info"],
        Element.CONTRARY: lambda: "==Checkpoint_%s failed_%s todavía está en la página==" % (
            kw["info"], kw["element_info"]),
        Element.CONTRARY_GETVAL: lambda: "==Error en los datos de Checkpoint_Comparison, los datos recuperados actualmente son: %s, los datos históricos recuperados son: %s" % (
            kw["current"], kw["history"]),
        Element.DEFAULT_CHECK: lambda: "==Checkpoint_%s falló, por favor check_%s ====" % (
            kw["info"], kw["element_info"]),
        Element.COMPARE: lambda: "==Los datos de Checkpoint_Comparison fallaron, los datos recuperados actualmente son: %s, los datos históricos recuperados son: %s" % (
            kw["current"], kw["history"]),
        Element.TOAST: lambda: "==Checkpoint_%s_Failed to find the popup box==" % kw["element_info"]
    }
    return elements[kw["type"]]()
