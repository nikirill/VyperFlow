import ast

from vyper.exceptions import (
    StructureException
)

def new_cons(llb, rlb, pos) :
    return {"left":llb, "right" : rlb, "pos" : pos}

def pos_printer(pos) :
# pos = (lineno, coloffset)
    return str(pos[0]) + "," + str(pos[1]) + "-" + str(pos[1]) if pos is not None else ""

def pos_str(pos) :
    return "L" + str(pos[0]) + "C" + str(pos[1]) if pos is not None else ""

def eval_label(exp, IFLs) :
    print("eval %s" % exp)
    if isinstance(exp, ast.Name) :
        ppls = exp.id.strip().split("_")
    elif type(exp) == str :
        ppls = exp.strip().split("_")
    else :
        raise StructureException("label must be type ast.Name: %s")
    rnt = {"meet" : False, "principals":[]}
    for ppl in ppls :
        pname = principal_trans(ppl)
        if pname not in ppls :
            IFLs[pname] = {"pos" : None, "const" : True}
        rnt["principals"].append(pname)
    print("eval done")
    return rnt, IFLs

def is_principal(s) :
    return s[0] == '@'

def principal_trans(s) :
    return "@" + s

def to_sherrlocname(s) :
    if s[0] == "@" :
        return "P_" + s[1:]
    else :
        return s

def to_sherrlocexp(exp) :
    if type(exp) == str :
        return to_sherrlocname(exp)
    print(exp)
    ppls = set([to_sherrlocname(s) for s in exp["principals"]])
    if len(ppls) == 1 :
        return [x for x in ppls][0]
    else :
        op = " ⊓ " if exp["meet"] else " ⊔ "
        return "(" + op.join(ppls) + ")"

