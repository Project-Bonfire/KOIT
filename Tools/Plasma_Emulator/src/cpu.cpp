/*--------------------------------------------------------------------
 * TITLE: Text Based User Interface
 * AUTHOR: Karl Janson
 * DATE CREATED: 14.12.16
 * FILENAME: cpu.cpp
 * PROJECT: Bonfire NoC CPU Emulator
 * COPYRIGHT: Software placed into the public domain by the author.
 *    Software 'as is' without warranty.  Author liable for nothing.
 * DESCRIPTION:
 *    Text user interface
 *--------------------------------------------------------------------*/

#include <iostream>
#include "command.h"
#include "common.h"
#include "cpu.h"
#include "memory.h"
#include "memory_ctrl.h"
#include "cpu_state.h"


CPU::CPU()
{
    cpu_state = new CPU_State;
}

CPU_State* CPU::state()
{
    return cpu_state;
}

CPU::~CPU()
{
    delete cpu_state;
}
