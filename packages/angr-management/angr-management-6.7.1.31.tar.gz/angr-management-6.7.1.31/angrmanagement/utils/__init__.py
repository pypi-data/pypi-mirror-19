
import itertools


def locate_function(inst, addr):
    """
    Locate the function that contains the address.

    :param inst:
    :param int addr: The address.
    :return: The function object or None if address is not inside any function.
    :rtype: angr.knowledge.Function or None
    """

    if inst.cfg is None:
        return None

    functions = inst.cfg.functions
    for _, function in functions.iteritems():
        for block in function.blocks:
            if block.addr <= addr < block.addr + block.size:
                return function

    return None

def get_label_text(addr, kb, function=None):

    if addr in kb.labels:
        return kb.labels[addr] + ":"

    # default case
    if function is not None and addr == function.addr:
        s = [ ]
        if function.name:
            s.append("%s:" % function.name)
        else:
            s.append("sub_%x:" % function.addr)
        if function.is_simprocedure:
            s.append('[SimProcedure]')
        if function.is_plt:
            s.append('[PLT]')
        return "\n".join(s)
    else:
        return "loc_%#x:" % addr


def get_block_objects(disasm, nodes):
    """
    Get a list of instructions and labels to be displayed in a block in disassembly view.

    :param angr.analyses.Disassembly disasm: The angr Disassembly Analysis instance.
    :param iterable nodes: A collection of CFG nodes.
    :return: a list of Instruction objects and label names (strings).
    :rtype: list
    """

    block_addrs = [node.addr for node in nodes]
    insn_addrs = list(itertools.chain.from_iterable(disasm.block_to_insn_addrs[addr] for addr in block_addrs))

    lst = [ ]
    for insn_addr in insn_addrs:
        if insn_addr in disasm.kb.labels:
            lst.append((insn_addr, disasm.kb.labels[insn_addr] + ":"))
        lst.append(disasm.raw_result_map['instructions'][insn_addr])

    if lst and not isinstance(lst[0], tuple):
        # the first element should be a label
        lst.insert(0, (block_addrs[0], get_label_text(block_addrs[0], disasm.kb)))

    return lst

def get_out_branches(supernode):
    """
    Get a list of descriptors of branches going out from the supernode.

    :param SuperCFGNode supernode: The node to work with.
    :return: A list of out branch descriptors.
    :rtype: list
    """

    return supernode.out_branches

def address_to_text(addr, kb):
    """
    Properly convert an address to text for a label.

    :param int addr: The address to convert.
    :param angr.KnowledgeBase kb: The knowledgebase in use.
    :return: Text representation of the address.
    :rtype: str
    """

    if addr in kb.labels:
        return kb.labels[addr]

    return "loc_%#x" % addr

def jump_to_address(disasm_wk, addr):
    """
    Jump to an address in a disassembly workspace.

    :param disasm_wk: The disassembly workspace.
    :param int addr: The address to jump to.
    :return: True if successfully jumped, False otherwise.
    :rtype: bool
    """

    function = locate_function(disasm_wk.inst, addr)
    if function is not None:
        disasm_wk.selected_function = function
        disasm_wk.highlighted_insns = set([addr])
        return True
    else:
        return False

def get_out_branches_for_insn(out_branch_dict, ins_addr):

    if ins_addr not in out_branch_dict:
        return None

    out_branch_map = out_branch_dict[ins_addr]

    if len(out_branch_map) > 1 and 'default' in out_branch_map:
        # if there are more than one targets, we return the union of non-default out branches
        keys = out_branch_map.keys()
        out_branch = None
        for k in keys:
            if k == 'default':
                continue
            out_branch = out_branch_map[k].copy() if out_branch is None else out_branch.merge(out_branch_map[k])

        return out_branch

    else:
        return next(out_branch_map.itervalues())

def get_string_for_display(memory_data):

    MAX_SIZE = 10

    if memory_data.content is not None:
        if memory_data.size > MAX_SIZE:
            return '"' + memory_data.content[:10] + '...\"'
        else:
            return '"' + memory_data.content + '"'
    else:
        return '<Unknown>'
